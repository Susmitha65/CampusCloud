import csv
from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import logging

from .models import Student, UploadedFile, Department, Classroom
from .forms import StudentEditForm
from tc.models import TcApplication

logger = logging.getLogger(__name__)

class ImportStudentsView(View):
    def get(self, request):
        return render(request, 'students/upload.html')

    def parse_date(self, date_str):
        for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y'):
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                pass
        return None

    def post(self, request):
        csv_file = request.FILES.get('csv_file')
        
        if not csv_file:
            messages.error(request, 'No file uploaded.')
            return render(request, 'students/upload.html')
        
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        
        for row in reader:
            date_of_birth = self.parse_date(row.get('Date of Birth', ''))
            date_of_join = self.parse_date(row.get('Date ofJoin', ''))
            student_data = {
                'name': row.get('Name', 'N/A'),
                'admission_number': row.get('Adm No.', '0'),
                'gender': row.get('Gender', 'Unknown'),
                'date_of_birth': date_of_birth,
                'date_of_join': date_of_join,
                'guardian': row.get('guardian', 'N/A'),
                'guardian_relation': row.get('Relashionship with guardian', 'Unknown'),
                'address': row.get('address', ''),
                'religion': row.get('Religion', 'Unknown'),
                'community': row.get('Caste', 'Unknown'),
                'category': row.get('Category', 'Unknown'),
                'feeconcession': row.get('Whether in receipt of fee concession', '').lower() in ('yes', 'true', '1'),
                'mobile': row.get('Mobile', ''),
                'photo': None,
                'registration_number': None,
                'department': None,
                'active': False,
                'data_verified': False
            }
            Student.objects.create(**student_data)
        
        # Save the uploaded file
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(csv_file.name, csv_file)
        file_url = fs.url(filename)
        
        # Save file information in the database
        UploadedFile.objects.create(file_name=csv_file.name, file_path=file_url)

        # Provide a success message
        messages.success(request, 'File successfully uploaded and students imported.')
        return render(request, 'students/upload.html')

class AllStudents(View):
    template_name = 'students/students.html'
    def get(self, request, *args, **kwargs):
        context = {'label': 'Students'}
        headers = {
            'name': "Name",
            'admission_number': "Admission Number",
            'registration_number': "Registration Number",
            'department': "Department",
            'action': "Actions",
        }
        if 'a_number' in request.GET and request.GET['a_number']:
            searchkey = request.GET['a_number']
            students_objs = Student.objects.filter(Q(name__icontains=searchkey) | Q(admission_number__icontains=searchkey)).order_by('admission_number')
        else:
            students_objs = Student.objects.all().order_by('admission_number')
        
        paginator = Paginator(students_objs, 10)
        page = request.GET.get('page')
        students = paginator.get_page(page)
        context['headers'] = headers
        context['students'] = students
        return render(request, self.template_name, context)

class StudentsPendingVerification(View):
    template_name = 'students/students.html'
    def get(self, request, *args, **kwargs):
        context = {'label': 'Students'}
        headers = {
            'name': "Name",
            'admission_number': "Admission Number",
            'registration_number': "Registration Number",
            'department': "Department",
            'action': "Actions",
        }
        filter_criteria = {'active': True, 'data_verified': False}
        if 'a_number' in request.GET and request.GET['a_number']:
            filter_criteria['admission_number'] = request.GET['a_number']
        
        students_objs = Student.objects.filter(**filter_criteria).order_by('admission_number')
        paginator = Paginator(students_objs, 10)
        page = request.GET.get('page')
        students = paginator.get_page(page)
        context['headers'] = headers
        context['students'] = students
        return render(request, self.template_name, context)

class VerifiedStudentView(View):
    template_name = 'students/students.html'
    def get(self, request, *args, **kwargs):
        context = {'label': 'Students'}
        headers = {
            'name': "Name",
            'admission_number': "Admission Number",
            'registration_number': "Registration Number",
            'department': "Department",
            'action': "Actions",
        }
        filter_criteria = {'active': True, 'data_verified': True}
        if 'a_number' in request.GET and request.GET['a_number']:
            filter_criteria['admission_number'] = request.GET['a_number']
        
        students_objs = Student.objects.filter(**filter_criteria).order_by('admission_number')
        paginator = Paginator(students_objs, 10)
        page = request.GET.get('page')
        students = paginator.get_page(page)
        context['headers'] = headers
        context['students'] = students
        return render(request, self.template_name, context)

class StudentDetailView(View):
    template_name = 'students/student.html'
    def get(self, request, *args, **kwargs):
        try:
            context = {}
            student_id = kwargs.get('pk')
            student = Student.objects.filter(pk=student_id).first()
            context['student'] = student
            tc_application = TcApplication.objects.filter(student_id=student_id)
            exists = tc_application.exists()
            if exists:
                context['tc_application'] = tc_application.first()
            context['tc_exists'] = exists
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error(e)
            return HttpResponseRedirect(reverse('students:students'))

class StudentEditView(View):
    template_name = 'students/edit_students.html'
    def get(self, request, *args, **kwargs):
        context = {}
        student_id = kwargs.pop('pk')
        student = Student.objects.filter(pk=student_id).first()
        form = StudentEditForm(instance=student)
        context['form'] = form
        context['label'] = "Edit Student"
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        student_id = kwargs.get('pk')
        student = Student.objects.filter(pk=student_id).first()
        form = StudentEditForm(request.POST, instance=student)
        if request.POST.get('data_verified') == 'on' and form.is_valid():
            form.save()
            if request.POST.get('applytc') == 'Save and apply TC':
                return HttpResponseRedirect(reverse('tc:apply_tc', args=(student_id,)))
            else:
                return HttpResponseRedirect(reverse('students:students'))
        else:
            context = {'form': form, 'label': "Edit Student"}
            return render(request, self.template_name, context)

def save_imported_students(request):
    if request.method == "POST":
        students = request.POST.getlist('students')
        for student_data in students:
            student = Student(**student_data)
            student.save()
        return redirect(reverse('students:student_list'))

    return redirect(reverse('students:import_students'))

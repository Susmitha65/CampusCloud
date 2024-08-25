from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import CustomUserForm, CustomUserCreationForm, StudentProfileForm
from django.contrib.auth.models import User
from students.models import Student
from tc.models import TcApplication
from .models import CustomUser
from django.views import View
from django.http import HttpResponseNotAllowed

# Student registration view
def student_register(request):
    # Logic for handling student registration
    return render(request, 'accounts/student_register.html')

# Custom logout view
def custom_logout(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('login')  # Redirect to your login page or another page
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

# Dashboard view
@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_teachers = 10  # Placeholder, update with real count if available
    total_tc_pending_applications = TcApplication.objects.filter(tc_issued=False).count()
    students_pending_verification = Student.objects.filter(data_verified=False).count()
    total_tc_issued = TcApplication.objects.filter(tc_issued=True).count()
    
    context = {
        'total_students': total_students,
        'total_tc_pending_applications': total_tc_pending_applications,
        'students_pending_verification': students_pending_verification,
        'total_tc_issued': total_tc_issued,
    }
    
    return render(request, 'dashboard.html', context)

# Register view for creating a new user
def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            user.save()
            if role == 'student':
                return redirect('account:register_student', user_id=user.id)  # Redirect to student profile registration
            else:
                return redirect('account:login')  # Redirect to login or another dashboard as per role
    else:
        form = CustomUserForm()
    
    return render(request, 'accounts/register.html', {'form': form})

# Register student profile after user creation
def register_student(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        student_form = StudentProfileForm(request.POST)

        # Debugging statements
        print("POST data received")
        print("User Form Valid:", user_form.is_valid())
        print("Student Form Valid:", student_form.is_valid())

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'student'
            user.save()

            student_profile = student_form.save(commit=False)
            student_profile.user = user
            student_profile.save()

            print("User and Student Profile created successfully")

            return redirect('account:student_login')  # Redirect to the student login page after successful registration
        else:
            print("Form data is invalid")
    else:
        user_form = CustomUserCreationForm()
        student_form = StudentProfileForm()

    return render(request, 'accounts/register_student.html', {
        'user_form': user_form,
        'student_form': student_form,
    })
# Student dashboard view
@login_required
def student_dashboard(request):
    return render(request, 'accounts/student_dashboard.html')

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account:student_dashboard')  # Redirect to student dashboard
        else:
            # Handle invalid login
            return render(request, 'accounts/student_login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'accounts/student_login.html')

import csv
from django.shortcuts import render
from django.core.files.storage import default_storage

def result_analysis(request):
    uploaded_data = None
    
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        file_path = default_storage.save(f'tmp/{csv_file.name}', csv_file)
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            uploaded_data = []
            for row in reader:
                # Assuming CSV has columns: student_name, department, subject, marks_obtained, total_marks
                percentage = (float(row['marks_obtained']) / float(row['total_marks'])) * 100
                uploaded_data.append({
                    'student_name': row['student_name'],
                    'department': row['department'],
                    'subject': row['subject'],
                    'marks_obtained': row['marks_obtained'],
                    'total_marks': row['total_marks'],
                    'percentage': round(percentage, 2),
                })

    return render(request, 'index.html', {'uploaded_data': uploaded_data, 'results': []})

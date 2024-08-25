from django.urls import path
from .views import (
    ImportStudentsView,
    AllStudents,
    StudentsPendingVerification,
    VerifiedStudentView,
    StudentDetailView,
    StudentEditView,
    save_imported_students
)

app_name = 'students'

urlpatterns = [
    path('upload/', ImportStudentsView.as_view(), name='upload_students'),
    path('all/', AllStudents.as_view(), name='all_students'),  # Ensure the name is 'all_students'
    path('pending_verification/', StudentsPendingVerification.as_view(), name='students_pending_verification'),
    path('verified/', VerifiedStudentView.as_view(), name='verified_students'),
    path('detail/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('edit/<int:pk>/', StudentEditView.as_view(), name='edit_student'),
    path('save_imported/', save_imported_students, name='save_imported_students'),
]

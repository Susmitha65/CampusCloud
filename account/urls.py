from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.custom_logout, name='logout'),
    path('student/register/', views.student_register, name='student_register'),
    path('register/student/<int:user_id>/', views.register_student, name='register_student'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('login/', views.student_login, name='student_login'),
]

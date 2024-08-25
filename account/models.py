from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('hod', 'HOD'),
        ('staff', 'Staff'),
        ('clerk', 'Clerk'),
        ('library', 'Library'),
        ('workshop', 'Workshop'),
    ]
    DEPARTMENT_CHOICES = [
        ('CHE', 'Chemical Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('IE', 'Industrial Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('EE', 'Electrical Engineering'),
    ]
    name = models.CharField(max_length=255, default='Anonymous')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # This avoids the conflict
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # This avoids the conflict
        blank=True,
    )

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    prn = models.CharField(max_length=20)
    admin_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.user.name

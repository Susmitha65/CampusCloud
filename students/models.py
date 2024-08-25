from django.db import models
from django.contrib.auth.models import User
from admin_tools.models import Department, AcademicSession,Classroom
# Create your models here.
relationship_type = (
    ('father','father'),
    ('mother','mother'),
    ('uncle','uncle'),
    )

gender_choice = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)


from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100, default='N/A')
    admission_number = models.CharField(max_length=50, default='0')
    gender = models.CharField(max_length=10, default='Unknown')
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_join = models.DateField(null=True, blank=True)
    guardian = models.CharField(max_length=100, default='N/A')
    guardian_relation = models.CharField(max_length=50, default='Unknown')
    address = models.TextField(default='')
    religion = models.CharField(max_length=50, default='Unknown')
    community = models.CharField(max_length=50, default='Unknown')
    category = models.CharField(max_length=50, default='Unknown')
    feeconcession = models.BooleanField(default=False)
    mobile = models.CharField(max_length=15, default='')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    registration_number = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=False)
    data_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['admission_number','department']
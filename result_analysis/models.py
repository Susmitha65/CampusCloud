from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks_obtained = models.IntegerField()
    total_marks = models.IntegerField()

    def percentage(self):
        return (self.marks_obtained / self.total_marks) * 100

    def __str__(self):
        return f"{self.student.name} - {self.subject}"

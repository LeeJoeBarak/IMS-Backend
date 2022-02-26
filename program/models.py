from django.db import models


# Create your models here.
from users.models import ProgramCoordinator,ProgramManager


class Program(models.Model):
    # "program name": "string",
    # "year": 0,
    # "semester": "string",
    # "program manager": "string",
    # "hours required": 0,
    # "depratment": "string"

    program = models.CharField(max_length=120, unique=True,primary_key=True)
    year = models.DateTimeField(auto_now=True)
    semester = models.CharField(max_length=2,default='A')
    programManager = models.ForeignKey(ProgramManager, on_delete=models.CASCADE)
    programCoordinator = models.ForeignKey(ProgramCoordinator, on_delete=models.CASCADE)
    prioritiesAmount = models.PositiveIntegerField()
    hoursRequired = models.PositiveIntegerField()
    department = models.CharField(max_length=100, default='A')

    def _str_(self):
        return self.title

# class Priority(models.Model):
#     Student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     internship = models.ForeignKey(Internships, on_delete=models.CASCADE)
#
# class Student(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     email = models.EmailField(max_length=100, unique=True)
#     phone_number = models.CharField(max_length=10)  # Numbers only, no room for a format like "(xxx) xxx-xxxx"
#     photo = models.ImageField(storage=photo_storage)
#     cv = models.FileField(upload_to=cv_storage)
#     status = student_status[0]  # student_status = ['candidate', 'advanced_candidate', 'intern']

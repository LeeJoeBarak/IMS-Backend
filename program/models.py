from django.db import models


# Create your models here.
from user.models import ProgramCoordinator, ProgramManager


class Program(models.Model):
    # "program name": "string",
    # "year": 0,
    # "semester": "string",
    # "program manager": "string",
    # "hours required": 0,
    # "depratment": "string"

    program = models.CharField(max_length=120, unique=True, primary_key=True)
    year = models.DateTimeField(auto_now=True)
    semester = models.CharField(max_length=2,default='A')
    programManager = models.OneToOneField(ProgramManager, on_delete=models.CASCADE, default='')
    programCoordinator = models.OneToOneField(ProgramCoordinator, on_delete=models.CASCADE, default='')
    prioritiesAmount = models.PositiveIntegerField()
    hoursRequired = models.PositiveIntegerField()
    department = models.CharField(max_length=100, default='Engine')


# class Priority(models.Model):
#     Student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     internship = models.ForeignKey(Internships, on_delete=models.CASCADE)
#

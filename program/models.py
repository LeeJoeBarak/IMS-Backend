from django.db import models
from djongo import models


# Create your models here.
from user.models import ProgramCoordinator, ProgramManager


class Program(models.Model):
    # "program name": "string",
    # "year": 0,
    # "semester": "string",
    # "program manager": "string",
    # "hours required": 0,
    # "depratment": "string"


    program = models.CharField(max_length=120, default='2020', primary_key=True)
    year = models.CharField(max_length=4, default='2020')
    semester = models.CharField(max_length=4, default='A')
    programManager = models.ForeignKey(ProgramManager, on_delete=models.CASCADE, default='')
    programCoordinator = models.OneToOneField(ProgramCoordinator, on_delete=models.CASCADE, default=None)
    prioritiesAmount = models.PositiveIntegerField(default=1)
    hoursRequired = models.PositiveIntegerField(default=100)
    department = models.CharField(max_length=100, default='Engine')


# class Priority(models.Model):
#     Student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     internship = models.ForeignKey(Internships, on_delete=models.CASCADE)
#

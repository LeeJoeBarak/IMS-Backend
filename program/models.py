from django.db import models
from djongo import models

# Create your models here.
from user.models import ProgramCoordinator, ProgramManager, Student, CompanyRepresentative, CompanyMentor
from django.contrib.auth.models import User


class Program(models.Model):
    # "program name": "string",
    # "year": 0,
    # "semester": "string",
    # "program manager": "string",
    # "hours required": 0,
    # "depratment": "string"
    # program_id = models.AutoField()
    program = models.CharField(max_length=120, default='2020', primary_key=True)
    year = models.CharField(max_length=4, default='2020')
    semester = models.CharField(max_length=4, default='A')
    # programManager = models.ForeignKey(ProgramManager, on_delete=models.CASCADE, default=None)
    # programCoordinator = models.OneToOneField(ProgramCoordinator, on_delete=models.CASCADE, default=None)
    prioritiesAmount = models.PositiveIntegerField(default=1)
    hoursRequired = models.PositiveIntegerField(default=100)
    department = models.CharField(max_length=100, default='Engine')
    status = models.CharField(max_length=6, default='True')


# Student:
class StudentAndProgram(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)


# ProgramManager:
class ProgramManagerAndProgram(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    programManager = models.ForeignKey(ProgramManager, on_delete=models.CASCADE)


# ProgramCoordinator:
class ProgramCoordinatorAndProgram(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    programCoordinator = models.OneToOneField(ProgramCoordinator, on_delete=models.CASCADE)



# CompanyRepresentative:
class CompanyRepresentativeAndProgram(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    companyRepresentative = models.OneToOneField(CompanyRepresentative, on_delete=models.CASCADE)


# CompanyMentor:
class CompanyMentorAndProgram(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    companyMentor = models.ForeignKey(CompanyMentor, on_delete=models.CASCADE)

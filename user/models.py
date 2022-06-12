from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from help_fanctions import student_status


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    status = models.CharField(default=student_status[0],
                              max_length=100)

    def __str__(self):
        return self.status


class Company(models.Model):
    companyName = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return "Company"


class CompanyMentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)

    def __str__(self):
        return "מנטור"


class CompanyRepresentative(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    companyName = models.CharField(max_length=100)

    def __str__(self):
        return "נציג חברה"


class ProgramManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return "מנהל תוכנית התמחות"


class ProgramCoordinator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return "רכז תוכנית התמחות"


class SystemManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return "מנהל מערכת"

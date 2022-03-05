from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from help_fanctions import student_status


class Student(models.Model):
    #     "username": "mayvaitz",
    #     "firstName": "may",
    #     "lastName": "vaitz",
    #     "password": "123456!",
    #     "email": "vaitz@post.bgu.ac.il"
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # email = models.EmailField(max_length=100, unique=True)
    status = models.CharField(default=student_status[0],
                              max_length=100)
    # student_status = ['candidate', 'advanced_candidate', 'intern']


class Company(models.Model):
    # "mentor": true,
    # "username": "mayvaitz",
    # "firstName": "may",
    # "lastName": "vaitz",
    # "password": "123456!",
    # "email": "vaitz@post.bgu.ac.il",
    # "companyName": "Elbit"

    companyName = models.CharField(max_length=100, primary_key=True)


class CompanyMentor(models.Model):
    # "mentor": true,
    # "username": "mayvaitz",
    # "firstName": "may",
    # "lastName": "vaitz",
    # "password": "123456!",
    # "email": "vaitz@post.bgu.ac.il",
    # "companyName": "Elbit"
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)


class CompanyRepresentative(models.Model):
    # "mentor": true,
    # "username": "mayvaitz",
    # "firstName": "may",
    # "lastName": "vaitz",
    # "password": "123456!",
    # "email": "vaitz@post.bgu.ac.il",
    # "companyName": "Elbit"
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    companyName = models.CharField(max_length=100)


class ProgramManager(models.Model):
    # "manager": true,
    # "username": "mayvaitz",
    # "firstName": "may",
    # "lastName": "vaitz",
    # "password": "123456!",
    # "email": "vaitz@post.bgu.ac.il"
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class ProgramCoordinator(models.Model):
    # "manager": false,
    # "username": "mayvaitz",
    # "firstName": "may",
    # "lastName": "vaitz",
    # "password": "123456!",
    # "email": "vaitz@post.bgu.ac.il"
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


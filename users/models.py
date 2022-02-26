from django.db import models

# Create your models here.
from django.contrib.auth.models import User, AbstractUser
import os
from django.conf import settings

from help_fanctions import student_status, photo_storage, cv_storage


def images_path():
    return os.path.join(settings.LOCAL_FILE_DIR, 'data\images')


def cv_path():
    return os.path.join(settings.LOCAL_FILE_DIR, 'data\cv')


# class Student_profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     email = models.EmailField(max_length=100, unique=True)
#     phone_number = models.CharField(max_length=10)  # Numbers only, no room for a format like "(xxx) xxx-xxxx"
#     # photo = models.ImageField(storage=photo_storage)
#     photo = models.FileField(verbose_name="Profile Picture",
#                              upload_to=images_path(),
#                              storage=photo_storage, max_length=255, null=True, blank=True)
#
#     cv = models.FileField(verbose_name="CV", upload_to=cv_path(),
#                           storage=cv_storage, null=True, blank=True)
#
#     status = student_status[0]  # student_status = ['candidate', 'advanced_candidate', 'intern']

class Student(models.Model):
    #     "username": "mayvaitz",
    #     "firstName": "may",
    #     "lastName": "vaitz",
    #     "password": "123456!",
    #     "email": "vaitz@post.bgu.ac.il"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # firstName = models.CharField(max_length=100)
    # lastName = models.CharField(max_length=100)
    # email = models.EmailField(max_length=100, unique=True)
    status = models.CharField(default=student_status[0], max_length=100)  # student_status = ['candidate', 'advanced_candidate', 'intern']


class Company(models.Model):
    # "mentor": true,
    # "username": "mayvaitz",
    # "firstName": "may",
    # "lastName": "vaitz",
    # "password": "123456!",
    # "email": "vaitz@post.bgu.ac.il",
    # "companyName": "Elbit"
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # mentor = models.BooleanField(default=True)
    # firstName = models.CharField(max_length=100)
    # lastName = models.CharField(max_length=100)
    # email = models.EmailField(max_length=100, unique=True)
    companyName = models.CharField(max_length=100, unique=True)


class Company_mentor(models.Model):
    # "mentor": true,
    # "username": "mayvaitz",
    # "firstName": "may",
    # "lastName": "vaitz",
    # "password": "123456!",
    # "email": "vaitz@post.bgu.ac.il",
    # "companyName": "Elbit"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # mentor = models.BooleanField(default=True)
    # firstName = models.CharField(max_length=100)
    # lastName = models.CharField(max_length=100)
    # email = models.EmailField(max_length=100, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Company_companyRepresentative(models.Model):
    # "mentor": true,
    # "username": "mayvaitz",
    # "firstName": "may",
    # "lastName": "vaitz",
    # "password": "123456!",
    # "email": "vaitz@post.bgu.ac.il",
    # "companyName": "Elbit"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # mentor = models.BooleanField(default=True)
    # firstName = models.CharField(max_length=100)
    # lastName = models.CharField(max_length=100)
    # email = models.EmailField(max_length=100, unique=True)
    companyName = models.ForeignKey(Company, on_delete=models.CASCADE)


class ProgramManager(models.Model):
    # "manager": true,
    # "username": "mayvaitz",
    # "firstName": "may",
    # "lastName": "vaitz",
    # "password": "123456!",
    # "email": "vaitz@post.bgu.ac.il"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # manager = models.BooleanField(default=True)
    # first_name = models.CharField(max_length=100)
    # lastName = models.CharField(max_length=100)
    # email = models.EmailField(max_length=100, unique=True)


class ProgramCoordinator(models.Model):
    # "manager": false,
    # "username": "mayvaitz",
    # "firstName": "may",
    # "lastName": "vaitz",
    # "password": "123456!",
    # "email": "vaitz@post.bgu.ac.il"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # manager = models.BooleanField(default=False)
    # first_name = models.CharField(max_length=100)
    # lastName = models.CharField(max_length=100)
    # email = models.EmailField(max_length=100, unique=True)

from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from help_fanctions import gradesSheet_storage, cv_storage, photo_storage, save_to_path, saves_paths
from user.models import Student, Company


# Create your models here.
class StudentProfile(models.Model):
    # "username": "string",V
    # "birthdate": "string",
    # "gitLink": "string",V
    # "linkedinLink": "string",
    # "picture": "string",V
    # "address": "string",
    # "cv": "string",V
    # "gradesSheet": "string"V
    username = models.ForeignKey(Student, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=10, blank=True)
    # Numbers only, no room for a format like "(xxx) xxx-xxxx"

    birthdate = models.DateTimeField(auto_now_add=True,  blank=True)

    gitLink = models.URLField(max_length=200, blank=True)

    linkedinLink = models.URLField(max_length=200, blank=True)

    address = models.CharField(max_length=200, blank=True)

    photo = models.FileField(verbose_name="Profile Picture",
                             upload_to=save_to_path(saves_paths['photo']),
                             storage=photo_storage, max_length=255, null=True, blank=True)

    cv = models.FileField(verbose_name="CV", upload_to=save_to_path(saves_paths['cv']),
                          storage=cv_storage, null=True, blank=True)

    gradesSheet = models.FileField(verbose_name="CV", upload_to=save_to_path(saves_paths['gradesSheet']),
                                   storage=gradesSheet_storage, null=True, blank=True)


class CompanyProfile(models.Model):
    # "username": "string",-not
    # "companyName": "string",
    # "yearEstablish": 0,
    # "workersAmount": 0,
    # "location": "string",
    # "about": "string"

    companyName = models.ForeignKey(Company, on_delete=models.CASCADE)
    yearEstablish = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
        help_text="Use the following format: <YYYY>", blank=True)
    workersAmount = models.PositiveIntegerField(default=1, blank=True)
    linkedinLink = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    about = models.CharField(max_length=500, blank=True)

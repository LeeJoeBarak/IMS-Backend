from django.db import models

# Create your models here.

from help_fanctions import intern_status_approved_hours_by_mentor, student_status_for_internship
from program.models import Program
from user.models import Company, CompanyRepresentative, CompanyMentor, Student


class Internship(models.Model):
    # todo: "username": "string",?????
    # "companyName": "string",
    # "internshipName": "string",
    # "about": "string",
    # "requirements": "string",
    # "mentor": "string"
    internshipName = models.CharField(max_length=120, primary_key=True)
    program = models.OneToOneField(Program, on_delete=models.CASCADE)
    companyRepresentative = models.ForeignKey(CompanyRepresentative, on_delete=models.CASCADE, default='')
    companyName = models.ForeignKey(Company, on_delete=models.CASCADE, default='')
    about = models.TextField(default="")
    requirements = models.TextField(default="")
    mentor = models.ForeignKey(CompanyMentor, on_delete=models.CASCADE, default='')
    isAssign = models.BooleanField(default=False)


class Priority(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    status_decision_by_company = models.CharField(default=student_status_for_internship[0],
                                                  max_length=100)
    status_decision_by_program_manager = models.CharField(default=student_status_for_internship[0],
                                                          max_length=100)


class AssignmentIntern(models.Model):
    # {
    #     "username": "string",
    #     "companyName": "string",
    #     "internshipName": "string",
    #     "studentsName": "string"
    # }
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)


class HoursReport(models.Model):
    #     "username": "string",
    #     "Intern": "string",
    #     "hours": [
    #         {
    #             "date": "string",
    #             "startTime": "string",
    #             "endTime": "string"
    #         }
    #     ]

    intern = models.ForeignKey(AssignmentIntern, on_delete=models.CASCADE, default='')
    student = models.OneToOneField(Student, on_delete=models.CASCADE, default='')
    mentor = models.OneToOneField(CompanyMentor, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    status = models.CharField(default=intern_status_approved_hours_by_mentor[0], max_length=100)

from django.db import models

# Create your models here.
from pip._internal.cli.cmdoptions import editable

from help_fanctions import intern_status_approved_hours_by_mentor, student_status_for_internship
from program.models import Program
from users.models import Company, Company_companyRepresentative, Company_mentor, Student


class Internship(models.Model):
    # todo: "username": "string",?????
    # "companyName": "string",
    # "internshipName": "string",
    # "about": "string",
    # "requirments": "string",
    # "mentor": "string"
    companyRepresentative = models.ForeignKey(Company_companyRepresentative, on_delete=models.CASCADE, default='')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, default='')
    internshipName = models.CharField(max_length=120)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default='')
    about = models.TextField(default="")
    requirements = models.TextField(default="")
    mentor = models.ForeignKey(Company_mentor, on_delete=models.CASCADE)
    isAssign = models.BooleanField(default=False)

    def _str_(self):
        return self.internshipName


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
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default='')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, default='')


class HoursReport(models.Model):
    # {
    #     "username": "string",
    #     "Intern": "string",
    #     "hours": [
    #         {
    #             "date": "string",
    #             "startTime": "string",
    #             "endTime": "string"
    #         }
    #     ]
    # }
    intern = models.ForeignKey(AssignmentIntern, on_delete=models.CASCADE, default='')
    # student = models.ForeignKey(Student, on_delete=models.CASCADE, default='')
    # mentor = models.ForeignKey(Company_mentor, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    status = models.CharField(default=intern_status_approved_hours_by_mentor[0], max_length=100)

    def _str_(self):
        return self.internshipName

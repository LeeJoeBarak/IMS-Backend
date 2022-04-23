from django.db import models

# Create your models here.

from help_fanctions import student_status_for_internship, reportByStudent_storage, save_to_path, saves_paths, \
    reportByMentor_storage
from program.models import Program
from user.models import Company, CompanyMentor, Student


# class Internship(models.Model):
#     # todo: "username": "string",?????
#     # "companyName": "string",
#     # "internshipName": "string",
#     # "about": "string",
#     # "requirements": "string",
#     # "mentor": "string"
#     internshipName = models.CharField(max_length=120, primary_key=True)
#     program = models.ForeignKey(Program, on_delete=models.CASCADE, default='')
#     # program = models.OneToOneField(Program, on_delete=models.CASCADE)
#     # companyRepresentative = models.ForeignKey(CompanyRepresentative, on_delete=models.CASCADE, default='')
#     companyName = models.ForeignKey(Company, on_delete=models.CASCADE, default='')
#     about = models.TextField(default="")
#     requirements = models.TextField(default="")
#     # mentor = models.ForeignKey(CompanyMentor, on_delete=models.CASCADE, default='')
#     isAssign = models.BooleanField(default=False)


class InternshipDetails(models.Model):
    internshipName = models.CharField(max_length=120, default='')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, default='')
    companyName = models.ForeignKey(Company, on_delete=models.CASCADE, default='')
    about = models.TextField(default="")
    requirements = models.TextField(default="")
    # mentor = models.ForeignKey(CompanyMentor, on_delete=models.CASCADE, default='')
    isAssign = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)


class Priority(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    internship = models.ForeignKey(InternshipDetails, on_delete=models.CASCADE, default='')
    status_decision_by_company = models.CharField(default=student_status_for_internship[0],
                                                  max_length=100)
    status_decision_by_program_manager = models.CharField(default=student_status_for_internship[0],
                                                          max_length=100)
    student_priority_number = models.PositiveIntegerField(default=1)


class AssignmentIntern(models.Model):
    # {
    #     "username": "string",
    #     "companyName": "string",
    #     "internshipName": "string",
    #     "studentsName": "string"
    # }
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    internship = models.ForeignKey(InternshipDetails, on_delete=models.CASCADE, default='')


class HoursReport(models.Model):
    # {
    #     "username": "string",
    #     "hours": [
    #         {
    #             "date": "string",
    #             "startTime": "string",
    #             "endTime": "string"
    #         }
    #     ]
    # }

    student = models.ForeignKey(Student, on_delete=models.CASCADE, default='')
    date = models.CharField(max_length=20, default='1.1.2020')
    startTime = models.CharField(max_length=20, default='08:00:00')
    endTime = models.CharField(max_length=20, default='20:00:00')
    approved = models.BooleanField(default=False)
    totalTime = models.CharField(max_length=20, default='20:00:00')


class InternshipAndMentor(models.Model):
    mentor = models.ForeignKey(CompanyMentor, on_delete=models.CASCADE)
    internship = models.ForeignKey(InternshipDetails, on_delete=models.CASCADE, default='')


class InternshipAndIntern(models.Model):
    intern = models.ForeignKey(Student, on_delete=models.CASCADE)
    internship = models.ForeignKey(InternshipDetails, on_delete=models.CASCADE, default='')


class InternReport(models.Model):
    # {
    #     "username": "string",
    #     "report": "string"
    # }

    intern = models.ForeignKey(Student, on_delete=models.CASCADE)
    report = models.FileField(verbose_name="reportByStudent",
                              upload_to=save_to_path(saves_paths['reportByStudent']),
                              storage=reportByStudent_storage, null=True, blank=True)


class MentorReport(models.Model):
    # {
    #     "username": "string",
    #     "Intern": "string",
    #     "report": "string"
    # }
    mentor = models.ForeignKey(CompanyMentor, on_delete=models.CASCADE)
    intern = models.ForeignKey(Student, on_delete=models.CASCADE)
    reportByMentor = models.FileField(verbose_name="reportByMentor",
                                      upload_to=save_to_path(saves_paths['reportByMentor']),
                                      storage=reportByMentor_storage, null=True, blank=True)



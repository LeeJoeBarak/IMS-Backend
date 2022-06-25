import os
import django
from rest_framework.test import APITestCase
# from rest_framework import status
import baker
from model_bakery import baker
# import json
from internship.models import *
from program.models import *
from user.models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ims_server.settings')
django.setup()


class TestStudent(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test_user_student", "test_user_student@test.io", "some_pass")
        self.student = Student.objects.create(user=self.user)

        self.user2 = User.objects.create_user("test_user_2", "test_user_2@test.io", "some_pass")
        self.student2 = Student.objects.create(user=self.user2, status="מועמד מתקדם")

        self.program = Program.objects.create(program="2022")

        self.company = Company.objects.create(companyName="test_company_1")
        self.internship_details_1 = baker.make(InternshipDetails, internshipName='test_internship_1',
                                               program=self.program, companyName=self.company)

        self.user = User.objects.create_user("test_user_companyRep", "test_user_companyRep@test.io", "some_pass")
        self.companyRep = CompanyRepresentative.objects.create(user=self.user)

    def test_student_model_str_status_0(self):
        self.assertEqual(str(self.student), 'סטודנט')

    def test_student_model_str_status_1(self):
        self.assertEqual(str(self.student2), 'מועמד מתקדם')



class TestCompany(APITestCase):
    pass


class TestCompanyMentor(APITestCase):
    pass


class TestCompanyRepresentative(APITestCase):
    pass


class TestProgramManager(APITestCase):
    pass


class TestProgramCoordinator(APITestCase):
    pass


class TestSystemManager(APITestCase):
    pass

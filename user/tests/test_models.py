import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ims_server.settings')

import django
django.setup()

import pytest
from rest_framework.test import APITestCase
from model_bakery import baker

from internship.models import *
from program.models import *
from user.models import *


class TestStudent(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test_user_student", "test_user_student@test.io", "some_pass")
        self.student = Student.objects.create(user=self.user)

        self.program = Program.objects.create(program="2022")

        self.company = Company.objects.create(companyName="test_company_1")
        self.internship_details_1 = baker.make(InternshipDetails, internshipName='test_internship_1', program=self.program, companyName=self.company)

        self.user = User.objects.create_user("test_user_companyRep", "test_user_companyRep@test.io", "some_pass")
        self.companyRep = CompanyRepresentative.objects.create(user=self.user)

    def test_student_model_str_status_0(self):
        self.assertEqual(str(self.student), 'סטודנט')

    # def test_student_model_str_status_1(self):
    #     # student_status = ['סטודנט', 'מועמד מתקדם', 'מתמחה']
    #     # todo - Not implemented yet
    #     data = {
    #         "username": str(self.companyRep.user.username),
    #         "program": str(self.program.pk),
    #         "approved": [
    #             {
    #                 "username": str(self.student.user.username),
    #                 "internship_id": str(self.internship_details_1.pk)
    #             }
    #         ]
    #     }
    #     response = self.client.post("/companyRep/setStatus", data, format='json')
    #     # print(f"=> student_model_str_status_1 DATA <= \n "
    #     #       f"XXXXXXXXXXXXXXXXX \n "
    #     #       f"XXXXXXXXXXXXXXXXX \n "
    #     #       f"XXXXXXXXXXXXXXXXX \n {response.data}")
    #     self.assertEqual(str(self.student), 'מועמד מתקדם')
    #
    # # def test_student_model_str_status_2(self):
    # #     # todo - Not implemented yet
    # #     self.assertEqual(str(self.student), 'מתמחה')


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



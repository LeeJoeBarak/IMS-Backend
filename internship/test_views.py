import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ims_server.settings')
import django

django.setup()
from rest_framework.test import APITestCase
from rest_framework import status
import baker
from model_bakery import baker
import json
from internship.models import *
from program.models import *
from user.models import *


class TestPostCreateInternshipByProgramManager(APITestCase):
    # POST /programManager/createInternship: True data
    def test_create_internship_true(self):
        # https://www.metacareers.com/v2/jobs/3162859397331113/
        sample_internship_data = {
            "program": "2030",
            "company": "Facebook",  # existing company
            "internshipName": "Software Engineer Intern",
            "mentor": "merav",
            "about": "Meta is seeking Software Engineer Interns  to join our engineering team. As a Software Engineer at Meta, you’ll drive the development of the systems behind Meta's products, create web applications that reach billions of people, build high volume servers and be a part of a team that’s working to help people connect with each other around the globe.",
            "requirements": "Develop and push production-ready code by quickly ramping on assigned codebase"}
        # print('sample_internship_data: ', sample_internship_data)
        response = self.client.post("/programManager/createInternship", sample_internship_data, format='json')
        # print('response.data: ', response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_internship_false(self):
        # https://www.metacareers.com/v2/jobs/3162859397331113/
        sample_internship_data = {
            "program": "2030",
            "company": "Facebook",  # existing company
            "internshipName": "Software Engineer Intern",
            "mentor": "meravvv",
            "about": "Meta is seeking Software Engineer Interns  to join our engineering team. As a Software Engineer at Meta, you’ll drive the development of the systems behind Meta's products, create web applications that reach billions of people, build high volume servers and be a part of a team that’s working to help people connect with each other around the globe.",
            "requirements": "Develop and push production-ready code by quickly ramping on assigned codebase"}
        print('sample_internship_data: ', sample_internship_data)
        response = self.client.post("/programManager/createInternship", sample_internship_data, format='json')
        print('response.data: ', response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPostCreateInternshipByCompanyRep(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("test_user_1", "test_user_1@test.io", "some_pass")
        self.compRep1 = CompanyRepresentative.objects.create(user=self.user1, companyName="abc")

    # POST /companyRep/createInternship
    def test_create_internship_true(self):
        # https://www.metacareers.com/v2/jobs/3162859397331113/
        sample_internship_data = {
            "username": "nevo",
            "program": "2030",
            "company": "Facebook",  # existing company
            "internshipName": "Software Engineer Intern",
            "mentor": "merav",
            "about": "Meta is seeking Software Engineer Interns  to join our engineering team. As a Software Engineer at Meta, you’ll drive the development of the systems behind Meta's products, create web applications that reach billions of people, build high volume servers and be a part of a team that’s working to help people connect with each other around the globe.",
            "requirements": "Develop and push production-ready code by quickly ramping on assigned codebase"}
        print('sample_internship_data: ', sample_internship_data)
        response = self.client.post("/companyRep/createInternship", sample_internship_data, format='json')
        print('response.data: ', response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_internship_false(self):
        sample_internship_data = {
            "username": "nevooo",
            "program": "2030",
            "company": "Facebook",  # existing company
            "internshipName": "Software Engineer Intern",
            "mentor": "merav",
            "about": "Meta is seeking Software Engineer Interns  to join our engineering team. As a Software Engineer at Meta, you’ll drive the development of the systems behind Meta's products, create web applications that reach billions of people, build high volume servers and be a part of a team that’s working to help people connect with each other around the globe.",
            "requirements": "Develop and push production-ready code by quickly ramping on assigned codebase"}
        print('sample_internship_data: ', sample_internship_data)
        response = self.client.post("/companyRep/createInternship", sample_internship_data, format='json')
        print('response.data: ', response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestGetInternship(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("test_user_1", "test_user_1@test.io", "some_pass")
        self.student1 = Student.objects.create(user=self.user1)

        self.user2 = User.objects.create_user("test_user_2", "test_user_2@test.io", "some_pass")
        self.student2 = Student.objects.create(user=self.user2, status="מועמד מתקדם")

        self.program = Program.objects.create(program="2022")

        self.company1 = Company.objects.create(companyName="test_company_1")
        self.internship_details_1 = baker.make(InternshipDetails, internshipName='test_internship_1',
                                               program=self.program, companyName=self.company1)
        self.company2 = Company.objects.create(companyName="test_company_2")
        self.internship_details_2 = baker.make(InternshipDetails, internshipName='test_internship_2',
                                               program=self.program, companyName=self.company2)

    # GET /internships/{program}
    def test_get_internships_by_program(self):
        response = self.client.get(f"/internships/{self.program.pk}", format='json')
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(resp), 2)
        for i, internship in enumerate(resp):
            self.assertEqual(resp[i], internship)

    # GET /companies/{program}
    def test_get_companies_by_program(self):
        response = self.client.get(f"/companies/{self.program.pk}", format='json')
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(resp), 2)
        for i, internship in enumerate(resp):
            self.assertEqual(resp[i], internship)


class TestPostInternshipsPrioritiesByCandidate(APITestCase):
    def setUp(self):
        self.user2 = User.objects.create_user("test_user_2", "test_user_2@test.io", "some_pass")
        self.student2 = Student.objects.create(user=self.user2, status="מועמד מתקדם")

        self.program = Program.objects.create(program="2022")

        self.student_and_program = baker.make(StudentAndProgram, program=self.program, student=self.student2)

        self.company1 = Company.objects.create(companyName="test_company_1")
        self.internship_details_1 = baker.make(InternshipDetails, internshipName='test_internship_1',
                                               program=self.program, companyName=self.company1)
        self.company2 = Company.objects.create(companyName="test_company_2")
        self.internship_details_2 = baker.make(InternshipDetails, internshipName='test_internship_2',
                                               program=self.program, companyName=self.company2)

    def test_post_candidate_priorities(self):
        data = {
            "username": str(self.student2.user.username),
            "priorities": [
                {
                    "internshipName": str(self.internship_details_1.internshipName),
                    "companyName": str(self.company1.companyName)
                },
                {
                    "internshipName": str(self.internship_details_2.internshipName),
                    "companyName": str(self.company2.companyName)
                }
            ]
        }
        response = self.client.post("/candidate/internshipsPriorities", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_username_post_candidate_priorities(self):
        data = {
            "username": str(self.student2.user.username),
            "priorities": [
                {
                    "internshipName": str(self.internship_details_1.pk),
                    "companyName": str(self.company1.companyName)
                },
                {
                    "internshipName": str(self.internship_details_2.pk),
                    "companyName": str(self.company2.companyName)
                }
            ]
        }
        response = self.client.post("/candidate/internshipsPriorities", data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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

# Fixtures are little pieces of data that serve as the baseline for your tests.
class TestInternshipDetails(APITestCase):
    def setUp(self):
        self.program = Program.objects.create(program="2022")
        self.company = Company.objects.create(companyName="GM")

    def test_internship_details_model(self):
        internship_details = baker.make(InternshipDetails, internshipName='Embedded intern', program=self.program, companyName=self.company)
        # internship_details = InternshipDetails(internshipName='Embedded intern', program='2020', companyName='GM')
        # internship_details.save()

        # Check database
        new_internship_details = InternshipDetails.objects.get(internshipName='Embedded intern')
        self.assertEqual(new_internship_details, internship_details)
        # check model fields
        self.assertEqual(internship_details.internshipName, 'Embedded intern')
        self.assertEqual(internship_details.program.pk, '2022')
        self.assertEqual(internship_details.companyName.pk, 'GM')



class TestPriority(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test_user", "test_user@test.io", "some_pass")
        self.student = Student.objects.create(user=self.user)

        self.program = Program.objects.create(program="2022")

        self.company = Company.objects.create(companyName="test_company_1")
        self.internship_details_1 = baker.make(InternshipDetails, internshipName='test_internship_1', program=self.program, companyName=self.company)
        self.company = Company.objects.create(companyName="test_company_2")
        self.internship_details_2 = baker.make(InternshipDetails, internshipName='test_internship_2', program=self.program, companyName=self.company)

    def test_priority_model(self):
        priority1 = baker.make(Priority, internship=self.internship_details_1, Student=self.student, student_priority_number=1)
        priority2 = baker.make(Priority, internship=self.internship_details_2, Student=self.student, student_priority_number=2)
        new_priorities = Priority.objects.filter(Student=self.student)

        # validate count() == 2
        self.assertEqual(new_priorities.count(), 2)



class TestAssignmentIntern(APITestCase):
    pass


class TestHoursReport(APITestCase):
    pass


class TestInternshipAndMentor(APITestCase):
    pass


class TestInternshipAndIntern(APITestCase):
    pass


class TestInternReport(APITestCase):
    pass


class TestMentorReport(APITestCase):
    pass


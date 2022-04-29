import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ims_server.settings')

import django
django.setup()

import pytest
from rest_framework.test import APITestCase
from model_bakery import baker

from internship.models import InternshipDetails
from program.models import Program
from user.models import Company

# Fixtures are little pieces of data that serve as the baseline for your tests.
class TestInternshipDetails(APITestCase):
    def setUp(self):
        self.program = Program.objects.create(program="2022")
        print(self.program)

        self.company = Company.objects.create(companyName="GM")
        print(self.company)

    def test_internship_details_model(self):
        # programs = Program.objects.all()
        # program = programs.filter(program='2020')
        # program = Program.objects.get(program='2020')

        internship_details = baker.make(InternshipDetails, internshipName='Embedded intern', program=self.program, companyName=self.company)
        # internship_details = InternshipDetails(internshipName='Embedded intern', program='2020', companyName='GM')
        internship_details.save()

        # Check database
        new_internship_details = InternshipDetails.objects.get(internshipName='Embedded intern')
        self.assertEqual(new_internship_details, internship_details)
        # check model fields
        self.assertEqual(internship_details.internshipName, 'Embedded intern')
        self.assertEqual(internship_details.program.pk, '2022')
        self.assertEqual(internship_details.companyName.pk, 'GM')



class TestPriority(APITestCase):
    pass


class TestAssignmentIntern(APITestCase):
    pass


class TestHoursReport(APITestCase):
    pass


class Test(APITestCase):
    pass


class Test(APITestCase):
    pass


class Test(APITestCase):
    pass


class Test(APITestCase):
    pass


class Test(APITestCase):
    pass
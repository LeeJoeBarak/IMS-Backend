import os
import django
from rest_framework.test import APITestCase
# from rest_framework import status
import baker
from model_bakery import baker
import json
# from internship.models import *
from program.models import *
# from user.models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ims_server.settings')
django.setup()


class TestGetInformationAboutProgram(APITestCase):
    def setUp(self):
        # self.program = Program.objects.create(program="test")
        self.program_test = baker.make(Program, program="program_test", year='2022', semester='B', prioritiesAmount=2,
                                       hoursRequired=160, department='Computer')

    # GET /prioritiesAmount/{program}:True data
    def test_get_priorities_amount_by_program_true_data(self):
        response = self.client.get(f"/prioritiesAmount/{self.program_test.pk}", format='json')
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp, 2)

    # GET /prioritiesAmount/{program}:False data
    def test_get_priorities_amount_by_program_false_data(self):
        response = self.client.get(f"/prioritiesAmount/{self.program_test.pk}", format='json')
        resp = json.loads(response.content.decode('utf-8'))
        self.assertIsNot(resp, 5)

    # GET /hoursRequired/{program}:True data
    def test_get_hours_required_by_program_true_data(self):
        response = self.client.get(f"/hoursRequired/{self.program_test.pk}", format='json')
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp, 160)

    # GET /hoursRequired/{program}:False data
    def test_get_hours_required_by_program_false_data(self):
        response = self.client.get(f"/hoursRequired/{self.program_test.pk}", format='json')
        resp = json.loads(response.content.decode('utf-8'))
        self.assertIsNot(resp, 161)

    # GET /activePrograms:True data
    def test_get_active_program_true_data(self):
        response = self.client.get(f"/activePrograms", format='json')
        resp = json.loads(response.content.decode('utf-8'))
        location = len(resp)
        self.assertEqual(resp[location-1], 'program_test')

    # GET /activePrograms:False data
    def test_get_active_program_false_data(self):
        response = self.client.get(f"/activePrograms", format='json')
        resp = json.loads(response.content.decode('utf-8'))
        location = len(resp)
        self.assertIsNot(resp[location-1], 'program')

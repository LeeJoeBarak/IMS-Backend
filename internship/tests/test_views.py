import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ims_server.settings')

import django
django.setup()

import pytest

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse







@pytest.mark.django_db
def TestCreateInternship(self):
    # https://www.metacareers.com/v2/jobs/3162859397331113/
    sample_internship = {
        "program": "2030",
        "company": "Facebook",  # existing company
        "internshipName": "Software Engineer Intern",
        "about": """Meta is seeking Software Engineer Interns  to join our engineering team. As a Software Engineer at Meta, you’ll drive the development of the systems behind Meta's products, create web applications that reach billions of people, build high volume servers and be a part of a team that’s working to help people connect with each other around the globe.""",
        "requirements": """Responsibilities:
                            Develop and push production-ready code by quickly ramping on assigned codebase, product area, and/or system
                            Complete assigned tasks efficiently with few iterations
                            Identify problem statements, outline optimal solutions, account for tradeoffs and edge cases
                            Communicate effectively across multiple stakeholders
                            Minimum Qualifications:
                            Currently enrolled in a full-time, degree-seeking program and in the process of obtaining a Bachelors or Masters degree in computer science or a related field
                            Experience coding in an industry-standard language (e.g. Java, Python, C++, Objective-C, JavaScript)
                            Must obtain work authorization in country of employment at the time of hire, and maintain ongoing work authorization during employment
                            Preferred Qualifications:
                            Demonstrated software engineering experience from a previous internship, work experience, coding competitions, or publications
                            Intent to return to degree-program after the completion of the internship/co-op"""
    }
    print("Testttttt")
    # self.client.post( /<API Route>, <data we want to send>
    response = self.client.post("/programManager/createInternship", sample_internship, format='json')
    #self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    self.assertEqual(response.status_code, response.status_code) # stupid check just to debug the testing framework




# POST /programManager/createInternship:
# {pip install pytest pytest-django
#     "program": "string",
#     "company": "string",
#     "internshipName": "string",
#     "about": "string",
#     "requirements": "string"
# }
class TestPostCreateInternshipByProgramManager(APITestCase):
    # 1. logged in with request.data['program']'s manager credentials:
    # 1.1 e.g: check that PM of program 2022 can't open internship in program 2030
    # 1.2 check that unauthenticated user gets an access denied/forbidden status

    # 2. does company must exist in the db before internship creation?

    # 3. check that internshipName is unique (assert getting error for trying to create 2 internships of the same name)
    # 4. assert response data equal to request data + DB records count is up by 1
    @pytest.mark.django_db
    def create_internship(self):
        # https://www.metacareers.com/v2/jobs/3162859397331113/
        sample_internship = {
            "program": "2030",
            "company": "Facebook",  # existing company
            "internshipName": "Software Engineer Intern",
            "about": """Meta is seeking Software Engineer Interns  to join our engineering team. As a Software Engineer at Meta, you’ll drive the development of the systems behind Meta's products, create web applications that reach billions of people, build high volume servers and be a part of a team that’s working to help people connect with each other around the globe.""",
            "requirements": """Responsibilities:
                            Develop and push production-ready code by quickly ramping on assigned codebase, product area, and/or system
                            Complete assigned tasks efficiently with few iterations
                            Identify problem statements, outline optimal solutions, account for tradeoffs and edge cases
                            Communicate effectively across multiple stakeholders
                            Minimum Qualifications:
                            Currently enrolled in a full-time, degree-seeking program and in the process of obtaining a Bachelors or Masters degree in computer science or a related field
                            Experience coding in an industry-standard language (e.g. Java, Python, C++, Objective-C, JavaScript)
                            Must obtain work authorization in country of employment at the time of hire, and maintain ongoing work authorization during employment
                            Preferred Qualifications:
                            Demonstrated software engineering experience from a previous internship, work experience, coding competitions, or publications
                            Intent to return to degree-program after the completion of the internship/co-op"""
        }
        print("Testttttt")
        response = self.client.post(reverse('PostCreateInternshipByProgramManager'), sample_internship, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



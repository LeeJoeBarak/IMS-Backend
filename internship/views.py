# import tables
# from django.contrib.sessions.backends import db
from django.http import JsonResponse
# from django.shortcuts import render
# from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
# from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.status import HTTP_404_NOT_FOUND

from program.models import Program, StudentAndProgram, ProgramManagerAndProgram
from program.serializers import ProgramNameSerializer, StudentAndProgramSerializers
from user.models import Company, CompanyRepresentative, Student, CompanyMentor
from user.serializer import UserDetailsSerializer, CompanyRepresentativeSerializer, CompanySerializer, \
    UserSerializer, StudentSerializer, MentorSerializer
from .serializers import InternshipsSerializer, CreateInternshipSerializer, InternshipIdSerializer, \
    InternshipsPrioritiesByCandidateSerializer, HoursReportSerializer, InternshipAndMentorSerializer, \
    AssignmentInternSerializer, InternshipAndInternSerializer, InternshipsFullSerializer

# from .serializers import InternshipsSerializer, NewInternshipSerializer, InternshipsPrioritiesByCandidateSerializer
from .models import Priority, InternshipDetails, AssignmentIntern, HoursReport, InternshipAndMentor, \
    InternshipAndIntern, InternReport, MentorReport
from rest_framework.response import Response
# from knox.models import AuthToken

import help_fanctions
from rest_framework import generics


class InternshipsView(viewsets.ModelViewSet):
    serializer_class = InternshipsSerializer
    queryset = InternshipDetails.objects.all()


# GET /internships/{program}
@api_view(['GET'])
def get_internships_by_program(request, program):
    if request.method == 'GET':
        internships = InternshipDetails.objects.all()
        internships = internships.filter(program=program)
        if not internships.exists():
            return Response('program not found', status=status.HTTP_404_NOT_FOUND)

        internships_serializer = InternshipsSerializer(internships, many=True)
        list_to_remove = ['program']
        help_fanctions.remove_info_from_serializer(list_to_remove, internships_serializer)
        # for i in internships_serializer.data:
        # internships_serializer.data[i] = db.main.users_company[]

        return JsonResponse(internships_serializer.data, safe=False)
        # 'safe=False' for objects serialization


# GET /programManager/{program}/{companyName}/{internshipName}/nominees:
# [
#     {
#         "username": "string",
#         "firstName": "string",
#         "lastName": "string",
#         "status": "string"
#     }
# ]
@api_view(['GET'])
def get_nominees_passed_company_interview(request, program, companyName, internshipName):
    if request.method == 'GET':
        student_details = []
        internship_obj = InternshipDetails.objects.filter(internshipName=internshipName,
                                                          program_id=program,
                                                          companyName_id=companyName)
        if not internship_obj.exists():
            return Response('company/internship not found', status=HTTP_404_NOT_FOUND)
        internship_serializer = InternshipIdSerializer(internship_obj, many=True)
        internship_serializer = list(internship_serializer.data)
        internship_serializer = internship_serializer[0]
        internship_id = internship_serializer['id']
        nominees = Priority.objects.filter(internship_id=internship_id)
        nominees_serializer = InternshipsPrioritiesByCandidateSerializer(nominees, many=True)
        nominees_serializer = list(nominees_serializer.data)
        for nominee in nominees_serializer:
            users = User.objects.all()
            user = users.filter(id=nominee['Student_id'])
            user_serializer = UserSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            username = user_serializer['username']
            firstName = user_serializer['first_name']
            lastName = user_serializer['last_name']
            students = Student.objects.all()
            student = students.filter(user_id=nominee['Student_id'])
            student_serializer = StudentSerializer(student, many=True)
            student_serializer = list(student_serializer.data)
            student_serializer = student_serializer[0]
            if nominee['status_decision_by_company'] == help_fanctions.student_status_for_internship[1]:
                student_detail = {
                    "username": username,
                    "firstName": firstName,
                    "lastName": lastName,
                    "assigned": nominee['status_decision_by_program_manager'] == 'true'
                }
                student_details.append(student_detail)
        return JsonResponse(student_details, safe=False)


# GET /companyRep/{username}/candidates:
# [
#     {
#         "username": "string",
#         "first_name": "string",
#         "last_name": "string",
#         "internship_id": "string",
#         "internship_name": "string",
#         "priority": 0
#     }
# ]
@api_view(['GET'])
def get_candidates_by_companyRep(request, program, companyName, internshipName):
    if request.method == 'GET':
        student_details = []
        internship_obj = InternshipDetails.objects.filter(internshipName=internshipName,
                                                          program_id=program,
                                                          companyName_id=companyName)
        if not internship_obj.exists():
            return Response('company/internship not found', status=HTTP_404_NOT_FOUND)
        internship_serializer = InternshipIdSerializer(internship_obj, many=True)
        internship_serializer = list(internship_serializer.data)
        internship_serializer = internship_serializer[0]
        internship_id = internship_serializer['id']
        nominees = Priority.objects.filter(internship_id=internship_id)
        nominees_serializer = InternshipsPrioritiesByCandidateSerializer(nominees, many=True)
        nominees_serializer = list(nominees_serializer.data)
        for nominee in nominees_serializer:
            users = User.objects.all()
            user = users.filter(id=nominee['Student_id'])
            user_serializer = UserSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            username = user_serializer['username']
            firstName = user_serializer['first_name']
            lastName = user_serializer['last_name']
            students = Student.objects.all()
            student = students.filter(user_id=nominee['Student_id'])
            student_serializer = StudentSerializer(student, many=True)
            student_serializer = list(student_serializer.data)
            student_serializer = student_serializer[0]
            if nominee['status_decision_by_company'] == help_fanctions.student_status_for_internship[1]:
                student_detail = {
                    "username": username,
                    "firstName": firstName,
                    "lastName": lastName,
                    "assigned": nominee['status_decision_by_program_manager']
                }
                student_details.append(student_detail)
        return JsonResponse(student_details, safe=False)


# assign to internship
@api_view(['GET'])
def get_nominees(request, program, companyName, internshipName):
    if request.method == 'GET':
        student_details = []
        internship_obj = InternshipDetails.objects.filter(internshipName=internshipName,
                                                          program_id=program,
                                                          companyName_id=companyName)
        if not internship_obj.exists():
            return Response('company/internship not found', status=HTTP_404_NOT_FOUND)
        internship_serializer = InternshipIdSerializer(internship_obj, many=True)
        # print('5. internship_serializer: ', internship_serializer.data)
        internship_serializer = list(internship_serializer.data)
        # print('6. internship_serializer: ', internship_serializer)
        internship_serializer = internship_serializer[0]
        # print('7. internship_serializer: ', internship_serializer)
        internship_id = internship_serializer['id']
        nominees = Priority.objects.filter(internship_id=internship_id)
        # InternshipsPrioritiesByCandidateSerializer
        nominees_serializer = InternshipsPrioritiesByCandidateSerializer(nominees, many=True)
        nominees_serializer = list(nominees_serializer.data)
        # program_id = program_serializer['program_id']
        # print('1. nominees_serializer: ', nominees_serializer)
        for nominee in nominees_serializer:
            # print('2. nominee: ', nominee)
            users = User.objects.all()
            user = users.filter(id=nominee['Student_id'])
            # print("3. user: ", user)
            user_serializer = UserSerializer(user, many=True)
            # print("3. user_serializer: ", user_serializer)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            username = user_serializer['username']
            firstName = user_serializer['first_name']
            lastName = user_serializer['last_name']
            # print('A. username: ', username)
            # print('B. firstName: ', firstName)
            # print('C. lastName: ', lastName)
            students = Student.objects.all()
            student = students.filter(user_id=nominee['Student_id'])
            student_serializer = StudentSerializer(student, many=True)
            student_serializer = list(student_serializer.data)
            student_serializer = student_serializer[0]
            if student_serializer["status"] == help_fanctions.student_status[1]:
                student_detail = {
                    "username": username,
                    "firstName": firstName,
                    "lastName": lastName,
                }
                student_details.append(student_detail)
        return JsonResponse(student_details, safe=False)


# GET /intern/getHours/{username}:
# [
#     {
#         "date": "string",
#         "startTime": "string",
#         "endTime": "string",
#         "approved": true
#     }
# ]
@api_view(['GET'])
def get_intern_hours(request, username):
    if request.method == 'GET':
        hours_details = []
        try:
            users = User.objects.all()
            user = users.filter(username=username)
            # if not user.exists():
            #     return Response('User not found - user', status=status.HTTP_404_NOT_FOUND)
            # print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            Student_id = user_serializer['id']
            # check if the user is a student:
            # student = Student.objects.get(user_id=Student_id)
            # print("2. student: ", student)
        except:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        hours = HoursReport.objects.filter(student_id=Student_id)
        hours_serializer = HoursReportSerializer(hours, many=True)
        hours_serializer = list(hours_serializer.data)
        for hour in hours_serializer:
            hour_details = {
                "id": hour['id'],
                "date": hour['date'],
                "startTime": hour['startTime'],
                "endTime": hour['endTime'],
                "approved": hour['approved'],
                "totalTime": hour['totalTime']
            }
            hours_details.append(hour_details)
        return JsonResponse(hours_details, safe=False)


# /mentor/getInterns/{username}
# [
#     {
#         "username": "string",
#         "first_name": "string",
#         "last_name": "string",
#         "email": "string",
#         "internship": "string"
#     }
# ]
@api_view(['GET'])
def get_interns_mentor(request, username):
    if request.method == 'GET':
        students_details = []
        try:
            users = User.objects.all()
            user = users.filter(username=username)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            mentor_id = user_serializer['id']
            # print("1. mentor_id: ", mentor_id)
            # check if the user is a mentor:
            mentor = CompanyMentor.objects.get(user_id=mentor_id)
            # print("2. mentor: ", mentor)
        except:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        internships = InternshipAndMentor.objects.filter(mentor_id=mentor_id)
        # print("2. internships: ", internships)
        internships_serializer = InternshipAndMentorSerializer(internships, many=True)
        internships_serializer = list(internships_serializer.data)

        for internship in internships_serializer:
            # AssignmentIntern
            assign_student = AssignmentIntern.objects.filter(internship_id=internship['internship_id'])
            assign_student_serializer = AssignmentInternSerializer(assign_student, many=True)
            assign_student_serializer = list(assign_student_serializer.data)
            for student in assign_student_serializer:
                users = User.objects.all()
                user = users.filter(pk=student['student_id'])
                user_serializer = UserSerializer(user, many=True)
                user_serializer = list(user_serializer.data)
                user_serializer = user_serializer[0]
                username_student = user_serializer['username']
                first_name_student = user_serializer['first_name']
                last_name_student = user_serializer['last_name']
                email_student = user_serializer['email']
                # username_student = user_serializer['username']
                # internshipName:
                internship_name = InternshipDetails.objects.filter(pk=internship['internship_id'])
                internship_name_serializer = InternshipsSerializer(internship_name, many=True)
                internship_name_serializer = list(internship_name_serializer.data)
                internship_name_serializer = internship_name_serializer[0]
                internshipName_student = internship_name_serializer['internshipName']
                student_details = {
                    "username": username_student,
                    "first_name": first_name_student,
                    "last_name": last_name_student,
                    "email": email_student,
                    "internship": internshipName_student,
                }
                students_details.append(student_details)
        return JsonResponse(students_details, safe=False)


# /companyRep/{username}/candidates/{program}:
# [
#     {
#         "username": "string",
#         "first_name": "string",
#         "last_name": "string",
#         "internship_id": "string",
#         "internship_name": "string",
#         "priority": 0
#     }
# ]
@api_view(['GET'])
def get_candidates_by_program_by_companyRep(request, username, program):
    if request.method == 'GET':
        students_details = []
        try:
            # check if the username is of a real CompanyRepresentative
            users = User.objects.all()
            user = users.filter(username=username)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            companyRep_id = user_serializer['id']
            # print("1. companyRep_id: ", companyRep_id)
            # check if the user is a mentor:
            companyRep = CompanyRepresentative.objects.filter(user_id=companyRep_id)
            # print("2. companyRep: ", companyRep)
        except:
            return Response('companyRep not found', status=HTTP_404_NOT_FOUND)
        # get company's CompanyRepresentative:
        # print("2. companyRep: ", companyRep)
        companyRepresentative = CompanyRepresentativeSerializer(companyRep, many=True)
        companyRepresentative = list(companyRepresentative.data)
        companyRepresentative = companyRepresentative[0]
        company = companyRepresentative['companyName']
        internships = InternshipDetails.objects.filter(program_id=program, companyName_id=company)
        # print("2. internships: ", internships)
        internships_serializer = InternshipsFullSerializer(internships, many=True)
        internships_serializer = list(internships_serializer.data)

        for internship in internships_serializer:
            students_priority = Priority.objects.filter(internship_id=internship['id'])
            students_priority_serializer = InternshipsPrioritiesByCandidateSerializer(students_priority, many=True)
            students_priority_serializer = list(students_priority_serializer.data)
            internship_id = internship['id']
            internship_name = internship['internshipName']
            for student in students_priority_serializer:
                users = User.objects.all()
                user = users.filter(pk=student['Student_id'])
                user_serializer = UserSerializer(user, many=True)
                user_serializer = list(user_serializer.data)
                user_serializer = user_serializer[0]
                username_student = user_serializer['username']
                first_name_student = user_serializer['first_name']
                last_name_student = user_serializer['last_name']
                priority = student['student_priority_number']
                status = student['status_decision_by_company']

                student_details = {
                    "username": username_student,
                    "first_name": first_name_student,
                    "last_name": last_name_student,
                    "internship_id": internship_id,
                    "internship_name": internship_name,
                    "priority": priority,
                    "status_decision_by_company": status == 'true'
                }
                students_details.append(student_details)
        return JsonResponse(students_details, safe=False)


# GET /mentor/{username}/candidates/{program}:
@api_view(['GET'])
def get_candidates_by_program_by_mentor(request, username, program):
    if request.method == 'GET':
        students_details = []
        try:
            # check if the username is of a real CompanyRepresentative
            users = User.objects.all()
            user = users.filter(username=username)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            mentor_id = user_serializer['id']
            # print("1. companyRep_id: ", companyRep_id)
            # check if the user is a mentor:
            mentor = CompanyMentor.objects.filter(user_id=mentor_id)
            # print("2. companyRep: ", companyRep)
        except:
            return Response('mentor not found', status=HTTP_404_NOT_FOUND)
        # get company's CompanyRepresentative:
        # print("2. companyRep: ", companyRep)
        mentor_serializer = MentorSerializer(mentor, many=True)
        mentor_serializer = list(mentor_serializer.data)
        mentor_serializer = mentor_serializer[0]
        company = mentor_serializer['company_id']
        internships = InternshipDetails.objects.filter(program_id=program, companyName_id=company)
        # print("2. internships: ", internships)
        internships_serializer = InternshipsFullSerializer(internships, many=True)
        internships_serializer = list(internships_serializer.data)

        for internship in internships_serializer:
            students_priority = Priority.objects.filter(internship_id=internship['id'])
            students_priority_serializer = InternshipsPrioritiesByCandidateSerializer(students_priority, many=True)
            students_priority_serializer = list(students_priority_serializer.data)
            internship_id = internship['id']
            internship_name = internship['internshipName']
            for student in students_priority_serializer:
                users = User.objects.all()
                user = users.filter(pk=student['Student_id'])
                user_serializer = UserSerializer(user, many=True)
                user_serializer = list(user_serializer.data)
                user_serializer = user_serializer[0]
                username_student = user_serializer['username']
                first_name_student = user_serializer['first_name']
                last_name_student = user_serializer['last_name']
                priority = student['student_priority_number']
                status = student['status_decision_by_company']

                student_details = {
                    "username": username_student,
                    "first_name": first_name_student,
                    "last_name": last_name_student,
                    "internship_id": internship_id,
                    "internship_name": internship_name,
                    "priority": priority,
                    "status_decision_by_company": status == 'true'
                }
                students_details.append(student_details)
        return JsonResponse(students_details, safe=False)


# GET /companies/{program}
# [
#     "string"
# ]
@api_view(['GET'])
def get_companies_by_program(request, program):
    if request.method == 'GET':
        try:
            program_id = Program.objects.get(pk=program)
            # print("1. program_id: ", program_id)
        except:
            return Response('program not found', status=HTTP_404_NOT_FOUND)

        company_list = InternshipDetails.objects.values_list('companyName_id', flat=True).order_by(
            'companyName_id').filter(program=program)
        companies = list(company_list)
        companies = set(companies)
        companies = list(companies)

        return JsonResponse(companies, safe=False)


# POST /programManager/createInternship:
# {
#     "program": "string",
#     "company": "string",
#     "internshipName": "string",
#     "about": "string",
#     "requirements": "string"
# # }
class PostCreateInternshipByProgramManager(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CreateInternshipSerializer

    def post(self, request):
        try:
            # create internship:
            # print('1. request.data: ', request.data)
            program = Program.objects.filter(pk=request.data['program'])
            # print('2. program: ', program[0])
            company = Company.objects.filter(pk=request.data['company'])
            # print('3. company: ', company[0])
            program_id = program[0]
            companyName_id = company[0]
        except:
            return Response('1.0Invalid company supplied / internshipName already exists', status.HTTP_401_UNAUTHORIZED)
        internshipName = InternshipDetails.objects.filter(internshipName=request.data['internshipName'],
                                                          program_id=program[0], companyName_id=company[0])
        # print('4. internshipName: ', internshipName)
        if len(internshipName) != 0:
            return Response('2. Invalid company supplied / internshipName already exists', status.HTTP_401_UNAUTHORIZED)

        internship = InternshipDetails.objects.create(
            program_id=ProgramNameSerializer(program_id, context=self.get_serializer_context()).data['program'],
            internshipName=request.data['internshipName'],
            companyName_id=CompanySerializer(companyName_id, context=self.get_serializer_context()).data['companyName'],
            about=request.data['about'],
            requirements=request.data['requirements']
        )
        # print("1. internship: ", internship.pk)

        try:
            users = User.objects.all()
            # mentor:
            user = users.filter(username=request.data['mentor'])
            if not user.exists():
                return Response('3. Invalid company supplied / internshipName already exists',
                                status.HTTP_401_UNAUTHORIZED)
            # print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            mentor_id = user_serializer['id']
            # print('2. mentor_id: ', mentor_id)
            # Check if the user is a mentor:
            mentor = CompanyMentor.objects.filter(user_id=mentor_id)
        except:
            return Response('4. Invalid company supplied / internshipName already exists', status.HTTP_401_UNAUTHORIZED)

        # "mentor": "string"
        # print("3. mentor_id: ", mentor_id)
        internship = InternshipDetails.objects.filter(pk=internship.pk)
        internship_serializer = CreateInternshipSerializer(internship, many=True)
        # print("3. internship_serializer: ", internship_serializer)
        internship_serializer = list(internship_serializer.data)
        internship_serializer = internship_serializer[0]
        internship_id = internship_serializer['id']

        internshipAndMentor = InternshipAndMentor.objects.create(
            internship_id=internship_id,
            mentor_id=mentor_id
        )

        print('4. internshipAndMentor: ', internshipAndMentor)

        return Response(
            content_type='successful create a internship request', status=status.HTTP_201_CREATED)


# POST /companyRep/createInternship
class PostCreateInternshipByCompanyRep(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CreateInternshipSerializer

    def post(self, request):
        try:
            # obj = AuthToken.objects.get(token_key=request.data['Authorization'])
            # print(obj)
            users = User.objects.all()
            user = users.filter(username=request.data['username'])
            # print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            # print("user_serializer: ", user_serializer)
            user_id = user_serializer['id']
            # print("22. user_serializer: ", user_serializer['id'])

            companyRepresentative = CompanyRepresentative.objects.all()
            companyRepresentative = companyRepresentative.filter(user_id=user_id)
            # companyRepresentative_s = CompanyRepresentative.objects.filter(user_id=user_id).first()
            companyRepresentative = CompanyRepresentativeSerializer(companyRepresentative, many=True)
            companyRepresentative = list(companyRepresentative.data)
            companyRepresentative = companyRepresentative[0]

            # print("companyRepresentative: ", companyRepresentative)
            company = companyRepresentative['companyName']
            # print("2. company: ", company)
            # create internship:
            # print('3. request.data: ', request.data)

            program = Program.objects.filter(pk=request.data['program'])
            # print('4. program: ', program[0])
            company = Company.objects.filter(pk=company)
            # print('5. company: ', company[0])
            program_id = program[0]
            companyName_id = company[0]
        except:
            return Response('Invalid username/program', status.HTTP_404_NOT_FOUND)

        internshipName = InternshipDetails.objects.filter(internshipName=request.data['internshipName'],
                                                          program_id=program[0], companyName_id=company[0])
        # print('4. internshipName: ', internshipName)
        if len(internshipName) != 0:
            return Response('Internship name supplied already exists',
                            status.HTTP_400_BAD_REQUEST)

        internship = InternshipDetails.objects.create(
            program_id=ProgramNameSerializer(program_id, context=self.get_serializer_context()).data['program'],
            internshipName=request.data['internshipName'],
            companyName_id=CompanySerializer(companyName_id, context=self.get_serializer_context()).data['companyName'],
            about=request.data['about'],
            requirements=request.data['requirements']
        )
        # print('5. internship: ', internship)

        try:
            users = User.objects.all()
            # mentor:
            user = users.filter(username=request.data['mentor'])
            if not user.exists():
                return Response('3. Invalid company supplied / internshipName already exists',
                                status.HTTP_401_UNAUTHORIZED)
            # print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            mentor_id = user_serializer['id']
            # print('2. mentor_id: ', mentor_id)
            # Check if the user is a mentor:
            mentor = CompanyMentor.objects.filter(user_id=mentor_id)
        except:
            return Response('4. Invalid company supplied / internshipName already exists', status.HTTP_401_UNAUTHORIZED)

        # "mentor": "string"
        # print("3. mentor_id: ", mentor_id)
        internship = InternshipDetails.objects.filter(pk=internship.pk)
        internship_serializer = CreateInternshipSerializer(internship, many=True)
        # print("3. internship_serializer: ", internship_serializer)
        internship_serializer = list(internship_serializer.data)
        internship_serializer = internship_serializer[0]
        internship_id = internship_serializer['id']

        internshipAndMentor = InternshipAndMentor.objects.create(
            internship_id=internship_id,
            mentor_id=mentor_id
        )

        return Response(
            content_type='successful create a internship request', status=status.HTTP_201_CREATED)


# POST /candidate/internshipsPriorities:
# {
#     "username": "string",
#     "priorities": [
#         {
#             "internshipName": "string",
#             "companyName": "string"
#         }
#     ]
# }
class PostInternshipsPrioritiesByCandidate(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CreateInternshipSerializer

    def post(self, request):
        internshipName_array = []

        try:
            users = User.objects.all()
            user = users.filter(username=request.data['username'])
            # print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            Student_id = user_serializer['id']
            # print('2. Student_id: ', Student_id)
            program = StudentAndProgram.objects.filter(student_id=Student_id)
            program_serializer = StudentAndProgramSerializers(program, many=True)
            program_serializer = list(program_serializer.data)
            program_serializer = program_serializer[0]
            program_id = program_serializer['program_id']
            # print('3. program_id: ', program_id)
            for internship in request.data['priorities']:
                # print('3. details: ', internship['internshipName'], program_id, internship['companyName'])
                internship_obj = InternshipDetails.objects.filter(internshipName=internship['internshipName'],
                                                                  program_id=program_id,
                                                                  companyName_id=internship['companyName'])
                # print('4. internship_obj: ', internship_obj)
                internship_serializer = InternshipIdSerializer(internship_obj, many=True)
                # print('5. internship_serializer: ', internship_serializer.data)
                internship_serializer = list(internship_serializer.data)
                # print('6. internship_serializer: ', internship_serializer)
                internship_serializer = internship_serializer[0]
                # print('7. internship_serializer: ', internship_serializer)
                internship_id = internship_serializer['id']
                # print('8. internship_obj: ', internship_obj)
                internshipName_array.append(internship_id)
                # print('9. internship_id: ', internship_id)

        except:
            return Response('Invalid username supplied (not exist)', status.HTTP_400_BAD_REQUEST)

        for i, val in enumerate(internshipName_array):
            # check if already priority exist, if not - create:
            # we do this check to save status_decision_by_company.
            try:
                # print('10. Student_id: ', Student_id)
                # print('11. internship_id: ', val)
                priority = Priority.objects.get(Student_id=Student_id, internship_id=val)
                # print('12. priority: ', priority)
                priority.student_priority_number = i + 1
                priority.save()
            except:
                priority = Priority.objects.create(
                    internship_id=val,
                    Student_id=Student_id,
                    student_priority_number=i + 1,
                )
                print('13. priority: ', priority)

        return Response(content_type='successful saved priorities', status=status.HTTP_200_OK)


# POST /assignIntern:
# {
#     "companyName": "string",
#     "internshipName": "string",
#     "username": "string"
# }
class UpdateStatusInternshipByManager(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        users = User.objects.all()
        user = users.filter(username=request.data['username'])
        if not user.exists():
            return Response('Invalid companyName\internshipName\studentName supplied', status=HTTP_404_NOT_FOUND)
        # print("1. user: ", user)
        user_serializer = UserDetailsSerializer(user, many=True)
        user_serializer = list(user_serializer.data)
        user_serializer = user_serializer[0]
        Student_id = user_serializer['id']
        # print('2. Student_id: ', Student_id)
        program = StudentAndProgram.objects.filter(student_id=Student_id)
        if not program.exists():
            return Response('Invalid companyName\internshipName\studentName supplied', status=HTTP_404_NOT_FOUND)
        program_serializer = StudentAndProgramSerializers(program, many=True)
        program_serializer = list(program_serializer.data)
        program_serializer = program_serializer[0]
        program_id = program_serializer['program_id']
        # print('3. program_id: ', program_id)
        internship_obj = InternshipDetails.objects.filter(internshipName=request.data['internshipName'],
                                                          program_id=program_id,
                                                          companyName_id=request.data['companyName'])
        if not internship_obj.exists():
            return Response('Invalid companyName\internshipName\studentName supplied', status=HTTP_404_NOT_FOUND)
        internship_serializer = InternshipIdSerializer(internship_obj, many=True)
        # print('5. internship_serializer: ', internship_serializer.data)
        internship_serializer = list(internship_serializer.data)
        # print('6. internship_serializer: ', internship_serializer)
        internship_serializer = internship_serializer[0]
        # print('7. internship_serializer: ', internship_serializer)
        internship_id = internship_serializer['id']
        # check if student already assign:
        priority_check = None
        try:
            priority_check = Priority.objects.get(
                status_decision_by_program_manager=help_fanctions.student_status_for_internship[1],
                internship_id=internship_id)
            if priority_check is not None:
                priority_check.status_decision_by_program_manager = help_fanctions.student_status_for_internship[0]
                priority_check.save()
        except:
            priority_check = None
        # update student status:
        # status_decision_by_program_manager
        priority = Priority.objects.get(Student_id=Student_id, internship_id=internship_id)
        priority.status_decision_by_program_manager = help_fanctions.student_status_for_internship[1]
        priority.save()

        return Response(
            content_type='successful set the student to the intern', status=status.HTTP_201_CREATED)


# POST /companyRep/setStatus:
# {
#     "username": "string",
#     "program": "string",
#     "approved": [
#         {
#             "username": "string",
#             "internship_id": "string"
#         }
#     ]
# }

class SetStatusByCompanyRep(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            users = User.objects.all()
            user = users.filter(username=request.data['username'])
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            companyRepresentative_id = user_serializer['id']
            CompanyRep = CompanyRepresentative.objects.filter(user_id=companyRepresentative_id)

            priorities = []
            for a in request.data['approved']:
                users = User.objects.all()
                user = users.filter(username=a['username'])
                # print("1. user: ", user)
                user_serializer = UserDetailsSerializer(user, many=True)
                user_serializer = list(user_serializer.data)
                user_serializer = user_serializer[0]
                Student_id = user_serializer['id']
                program = StudentAndProgram.objects.filter(program_id=request.data['program'], student_id=Student_id)
                if not program.exists():
                    return Response('Invalid username\companyName\internshipName\studentsName supplied',
                                    status=status.HTTP_401_UNAUTHORIZED)

                priority = Priority.objects.get(Student_id=Student_id, internship_id=a['internship_id'])
                priorities.append(priority)
            for p in priorities:
                p.status_decision_by_company = help_fanctions.student_status_for_internship[1]
                p.save()
        except:
            return Response('Invalid username\companyName\internshipName\studentsName supplied',
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            content_type='successful set the student status', status=status.HTTP_200_OK)


class SetStatusByMentor(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # print("0. request.data: ", request.data)
        try:
            # print("0. request.data: ", request.data)
            users = User.objects.all()
            user = users.filter(username=request.data['username'])
            # print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            mentor_id = user_serializer['id']
            mentor = CompanyMentor.objects.filter(user_id=mentor_id)

            priorities = []
            for a in request.data['approved']:
                users = User.objects.all()
                user = users.filter(username=a['username'])
                # print("2. user: ", user)
                user_serializer = UserDetailsSerializer(user, many=True)
                user_serializer = list(user_serializer.data)
                user_serializer = user_serializer[0]
                Student_id = user_serializer['id']
                program = StudentAndProgram.objects.filter(program_id=request.data['program'], student_id=Student_id)
                if not program.exists():
                    return Response('Invalid username\companyName\internshipName\studentsName supplied',
                                    status=status.HTTP_401_UNAUTHORIZED)

                priority = Priority.objects.get(Student_id=Student_id, internship_id=a['internship_id'])
                priorities.append(priority)
            for p in priorities:
                p.status_decision_by_company = help_fanctions.student_status_for_internship[1]
                p.save()
        except:
            return Response('Invalid username\companyName\internshipName\studentsName supplied - except',
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            content_type='successful set the student status', status=status.HTTP_200_OK)


# POST /setInterns:
# {
#     "programManager_username":"string"
#     "program": "string",
#     "new_interns": [
#         {
#             "username": "string",
#             "internship_id": "string"
#         }
#     ]
# }
class SetInternsToInternship(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            # check manager username:
            users = User.objects.all()
            user = users.filter(username=request.data['programManager_username'])

            print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            manager_id = user_serializer['id']
            print('2. manager_id: ', manager_id)
            # check program:
            program = ProgramManagerAndProgram.objects.filter(programManager_id=manager_id,
                                                              program=request.data['program'])
            program_serializer = StudentAndProgramSerializers(program, many=True)
            program_serializer = list(program_serializer.data)
            program_serializer = program_serializer[0]
            program_id = program_serializer['program_id']
            print('3. program_id: ', program_id)

            # students:
            for new_intern in request.data['new_interns']:
                print('4. in loop ', new_intern)
                users = User.objects.all()
                user = users.filter(username=new_intern['username'])
                print("5. user: ", user)
                user_serializer = UserDetailsSerializer(user, many=True)
                user_serializer = list(user_serializer.data)
                user_serializer = user_serializer[0]
                Student_id = user_serializer['id']
                program = StudentAndProgram.objects.filter(program_id=request.data['program'], student_id=Student_id)
                internship_obj = InternshipDetails.objects.filter(pk=new_intern['internship_id'])

                # Set intern:
                assignIntern = InternshipAndIntern.objects.filter(
                    intern_id=Student_id,
                    internship_id=new_intern['internship_id'])
                if assignIntern.exists():
                    # return Response('The assignment intern already exist', status=HTTP_404_NOT_FOUND)
                    continue
                InternshipAndIntern.objects.create(intern_id=Student_id, internship_id=new_intern['internship_id'])

                # 1. update student status:
                student = Student.objects.get(user_id=Student_id)
                student.status = help_fanctions.student_status[2]
                student.save()
                print('a. update student status')

                # 2. update internship isAssign:
                internship = InternshipDetails.objects.get(id=new_intern['internship_id'])
                # print('7. internship: ', internship)
                # print('6. internship.isAssign: ', internship.isAssign)
                internship.isAssign = True
                # print('7. After internship.isAssign: ', internship.isAssign)
                internship.save()
                print('b. update internship isAssign')

                # 3. update program status:
                program_obj = Program.objects.get(program=request.data['program'])
                program_obj.status = "True"
                program_obj.save()
                print('c. update program status')

        except:
            return Response('Invalid manager username\student username\program\internship_id supplied',
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            content_type='successful set all the students to interns', status=status.HTTP_201_CREATED)


# POST /intern/hoursReport:
# {
#     "username": "string",
#     "hours": [
#         {
#             "date": "string",
#             "startTime": "string",
#             "endTime": "string"
#             "totalTime": "string"
#         }
#     ]
# }
class HoursReportByIntern(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # print("request.data: ", request.data)
        # get student id:
        try:
            users = User.objects.all()
            user = users.filter(username=request.data['username'])
            if not user.exists():
                return Response('Invalid username supplied', status=status.HTTP_401_UNAUTHORIZED)
            # print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            Student_id = user_serializer['id']
            # check if the user is a student:
            student = Student.objects.get(user_id=Student_id)
        except:
            return Response('Invalid username supplied', status=status.HTTP_401_UNAUTHORIZED)
        # print('2. Student_id: ', Student_id)
        # print('3. hours:' , request.data['hours'])
        # Report hour:
        for hour in request.data['hours']:
            l_hour = dict(hour)
            # print('3. hours:' , request.data['hours'])
            checkHoursReport = HoursReport.objects.filter(student_id=Student_id, date=l_hour['date'],
                                                          startTime=l_hour['startTime'],
                                                          endTime=l_hour['endTime'])
            if checkHoursReport.exists():
                continue

            # change to this if there is an error
            # totalTime = float(l_hour['totalTime'])
            hoursReport = HoursReport.objects.create(
                student_id=Student_id,
                date=l_hour['date'],
                startTime=l_hour['startTime'],
                endTime=l_hour['endTime'],
                totalTime=l_hour['totalTime']
            )
            # print('A. date: ', l_hour['date'])
            # print('B. startTime: ', l_hour['startTime'])
            # print('C. endTime: ', l_hour['endTime'])
            # print("3. hoursReport: ", hoursReport)

        return Response(
            content_type='successful add the hours', status=status.HTTP_200_OK)


# POST /mentor/hoursApproval:
# {
#     "username": "string", - mentor
#     "intern": "string", - student
#     "hours": [ - id of hour report
#         "string"
#     ]
# }
class HoursApprovalByMentor(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # print("request.data: ", request.data)
        # get student id:
        try:
            # check if the username is a mentor and then if he is the mentor of the intern:
            users = User.objects.all()
            user = users.filter(username=request.data['username'])

            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            mentor_id = user_serializer['id']
            # print("1. mentor_id: ", mentor_id)

            # check if the user is a mantor:
            mentor = CompanyMentor.objects.get(user_id=mentor_id)
            # print("2. mentor: ", mentor)
            # get intern id:
            users = User.objects.all()
            user = users.filter(username=request.data['intern'])
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            intern_id = user_serializer['id']
            # print("3. inter_id: ", intern_id)
            # get internship id by intern:
            internshipAndIntern = InternshipAndIntern.objects.filter(intern_id=intern_id)
            internshipAndIntern_serializer = InternshipAndInternSerializer(internshipAndIntern, many=True)
            # print('4. internshipAndIntern_serializer: ', internshipAndIntern_serializer.data)
            internshipAndIntern_serializer = list(internshipAndIntern_serializer.data)
            # print('5. internshipAndIntern_serializer: ', internshipAndIntern_serializer)
            internshipAndIntern_serializer = internshipAndIntern_serializer[0]
            # print('6. internshipAndIntern_serializer: ', internshipAndIntern_serializer)
            internship_id_by_intern = internshipAndIntern_serializer['internship_id']
            # print('7. internship_id_by_intern: ', internship_id_by_intern)

            # get internship id by mentor:
            internships_id_mentor = InternshipAndMentor.objects.filter(mentor=mentor_id)
            # InternshipAndMentorSerializer
            internshipAndMentor_serializer = InternshipAndMentorSerializer(internships_id_mentor, many=True)
            internshipAndMentor_serializer = list(internshipAndMentor_serializer.data)
            for internshipAndMentor in internshipAndMentor_serializer:
                if internshipAndMentor['internship_id'] == internship_id_by_intern:
                    # update status:
                    hours = []
                    for hour in request.data['hours']:
                        hour_report = HoursReport.objects.get(id=hour)
                        hours.append(hour_report)
                    for hour in hours:
                        # print('7. internship: ', internship)
                        # print('6. internship.isAssign: ', internship.isAssign)
                        hour.approved = True
                        # print('7. After internship.isAssign: ', internship.isAssign)
                        hour.save()
        except:
            return Response('Invalid username/intern/hour id supplied', status=status.HTTP_401_UNAUTHORIZED)
        return Response(
            content_type='successful approve the hours', status=status.HTTP_200_OK)


# POST /intern/uploadReport:
# {
#     "username": "string",
#     "report": "string"
# }
class PostUploadReportByIntern(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, username):
        # print('uploadReport: ', username)
        try:
            users = User.objects.all()
            user = users.filter(username=username)
            # user = users.filter(username=request.data['username'])
            if not user.exists():
                return Response('Invalid username supplied', status=status.HTTP_401_UNAUTHORIZED)
            # print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            student_id = user_serializer['id']
            # print('2. student_id: ', student_id)
            # Check if the user is a student:
            student = Student.objects.filter(user_id=student_id)
            student_serializer = StudentSerializer(student, many=True)
            student_serializer = list(student_serializer.data)
            student_serializer = student_serializer[0]
            # Check if the student is an intern:
            # student_serializer['status']
            # print('3. status: ', student_serializer['status'])
            if student_serializer['status'] != help_fanctions.student_status[2]:
                return Response('Invalid username supplied', status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response('Invalid username', status.HTTP_401_UNAUTHORIZED)

        try:
            intern_report = InternReport.objects.get(intern_id=student_id)
            intern_report.report = request.data['report']
            intern_report.save()
            # print('4. intern_report: ', intern_report)

        except:
            # return Response('4. Invalid username', status.HTTP_401_UNAUTHORIZED)
            intern_report = InternReport.objects.create(
                report=request.data['report'],
                intern_id=student_id)
            intern_report.save()
            # print('5. intern_report: ', intern_report)
            return Response(content_type='successful upload', status=status.HTTP_200_OK)

        return Response(content_type='successful upload', status=status.HTTP_200_OK)


# POST /mentor/uploadReport
# {
#     "username": "string",
#     "intern": "string",
#     "report": "string"
# }
class PostUploadReportByMentor(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, username, intern):
        try:
            users = User.objects.all()
            # mentor:
            user = users.filter(username=username)
            if not user.exists():
                return Response('Invalid username supplied', status=status.HTTP_401_UNAUTHORIZED)
            # print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            mentor_id = user_serializer['id']
            # print('2. mentor_id: ', mentor_id)
            # Check if the user is a mentor:
            mentor = CompanyMentor.objects.filter(user_id=mentor_id)
            # print('3. mentor: ', mentor)
            # intern:
            user = users.filter(username=intern)
            if not user.exists():
                return Response('Invalid username/intern supplied', status=status.HTTP_401_UNAUTHORIZED)
            # print("4. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            student_id = user_serializer['id']
            # print('5. student_id: ', student_id)
            # Check if the user is a student:
            student = Student.objects.filter(user_id=student_id)
            student_serializer = StudentSerializer(student, many=True)
            student_serializer = list(student_serializer.data)
            student_serializer = student_serializer[0]
            # Check if the student is an intern:
            # student_serializer['status']
            # print('3. status: ', student_serializer['status'])
            if student_serializer['status'] != help_fanctions.student_status[2]:
                return Response('Invalid username/intern supplied', status=status.HTTP_401_UNAUTHORIZED)

            internshipAndIntern = InternshipAndIntern.objects.filter(intern_id=student_id)
            internshipAndIntern_serializer = InternshipAndInternSerializer(internshipAndIntern, many=True)
            internshipAndIntern_serializer = list(internshipAndIntern_serializer.data)
            internshipAndIntern_serializer = internshipAndIntern_serializer[0]
            internship_id_intern = internshipAndIntern_serializer['internship_id']
            # print('6. internship_id_intern: ', internship_id_intern)

            internshipAndMentor = InternshipAndMentor.objects.filter(mentor_id=mentor_id)
            internshipAndMentor_serializer = InternshipAndMentorSerializer(internshipAndMentor, many=True)
            internshipAndMentor_serializer = list(internshipAndMentor_serializer.data)
            internshipAndMentor_serializer = internshipAndMentor_serializer[0]
            internship_id_mentor = internshipAndMentor_serializer['id']
            # print('7. internship_id_mentor: ', internship_id_mentor)
            if internship_id_mentor != internship_id_intern:
                return Response('Invalid username/intern supplied', status=status.HTTP_401_UNAUTHORIZED)

        except:
            return Response('Invalid username/intern supplied', status=status.HTTP_401_UNAUTHORIZED)

        try:
            mentor_report = MentorReport.objects.get(intern_id=student_id)
            mentor_report.report = request.data['report']
            mentor_report.save()
            # print('8. mentor_report: ', mentor_report)

        except:
            # return Response('4. Invalid username', status.HTTP_401_UNAUTHORIZED)
            mentor_report = MentorReport.objects.create(
                report=request.data['report'],
                intern_id=student_id,
                mentor_id=mentor_id)
            mentor_report.save()
            # print('9. mentor_report: ', mentor_report)
            return Response(content_type='successful upload', status=status.HTTP_200_OK)

        return Response(content_type='successful upload', status=status.HTTP_200_OK)

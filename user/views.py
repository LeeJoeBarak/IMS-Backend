# import tables
# from django.shortcuts import render
# from django.contrib.sessions.backends import db
from django.http import JsonResponse
# from django.shortcuts import render
# from django.shortcuts import get_object_or_404
# from rest_framework import viewsets
from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework import status
from django.contrib.auth.models import User
# from django.contrib.auth.signals import user_logged_in, user_logged_out
from help_fanctions import student_status
from program.models import StudentAndProgram, CompanyMentorAndProgram, CompanyRepresentativeAndProgram, \
    ProgramManagerAndProgram, ProgramCoordinatorAndProgram
from program.serializers import StudentAndProgramSerializers, CompanyMentorAndProgramSerializers, \
    CompanyRepresentativeAndProgramSerializers, ProgramManagerAndProgramSerializers, \
    ProgramCoordinatorAndProgramSerializers
from .models import Company, ProgramManager, Student, CompanyMentor, CompanyRepresentative, ProgramCoordinator, \
    SystemManager
# from .serializer import CompanyRepresentativeSerializer

from rest_framework.response import Response
# import help_fanctions

from .serializer import CompanySerializer, UserDetailsSerializer, UserSerializer, StudentSerializer


# GET /companies
@api_view(['GET'])
def get_companies_list(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        companies_serializer = CompanySerializer(companies, many=True)
        return JsonResponse(companies_serializer.data, safe=False)


# GET /programManagers:
@api_view(['GET'])
# [
#     {
#         "id": 41,
#         "first_name": "Michal",
#         "last_name": "Ter"
#     },
#     {
#         "id": 49,
#         "first_name": "Erez",
#         "last_name": "Terme"
#     }
# ]
def get_program_managers(request):
    if request.method == 'GET':
        manager_list = ProgramManager.objects.values_list('user_id', flat=True).order_by('user_id')
        manager_list = list(manager_list)
        users = User.objects.filter(pk__in=manager_list)
        manager = UserDetailsSerializer(users, many=True)
        return JsonResponse(manager.data, safe=False)


# GET /users/details/{username}:
@api_view(['GET'])
# {
#     "firstName": "string",!!!
#     "userType": "string",
#     "program": "string"
# }

def get_details_about_user_by_username(request, username):
    if request.method == 'GET':
        users = User.objects.all()
        user = users.filter(username=username)
        # print(user)
        user_serializer = UserDetailsSerializer(user, many=True)
        user_serializer = list(user_serializer.data)
        user_serializer = user_serializer[0]
        # print("user_serializer: ", user_serializer)
        first_name = user_serializer['first_name']
        # print("user_serializer: ", user_serializer['first_name'])
        # print("user_serializer: ", user_serializer['last_name'])
        user_id = user_serializer['id']
        # print("user_serializer: ", user_serializer['id'])

        model = Student.objects.filter(user_id=user_id).first()
        if model is not None:
            program = StudentAndProgram.objects.filter(student_id=user_id).first()
            if program is not None:
                dataProgram = StudentAndProgramSerializers(program)
        if model is None:
            model = CompanyMentor.objects.filter(user_id=user_id).first()
            if model is not None:
                program = CompanyMentorAndProgram.objects.filter(companyMentor_id=user_id).first()
                if program is not None:
                    dataProgram = CompanyMentorAndProgramSerializers(program)
            if model is None:
                model = CompanyRepresentative.objects.filter(user_id=user_id).first()
                if model is not None:
                    program = CompanyRepresentativeAndProgram.objects.filter(companyRepresentative_id=user_id).first()
                    if program is not None:
                        dataProgram = CompanyRepresentativeAndProgramSerializers(program)
                if model is None:
                    model = ProgramManager.objects.filter(user_id=user_id).first()
                    if model is not None:
                        program = ProgramManagerAndProgram.objects.filter(programManager_id=user_id).first()
                        if program is not None:
                            dataProgram = ProgramManagerAndProgramSerializers(program)
                    if model is None:
                        model = ProgramCoordinator.objects.filter(user_id=user_id).first()
                        if model is not None:
                            program = ProgramCoordinatorAndProgram.objects.filter(programCoordinator_id=user_id).first()
                            if program is not None:
                                dataProgram = ProgramCoordinatorAndProgramSerializers(program)

                        if model is None:
                            model = SystemManager.objects.filter(user_id=user_id).first()
                            # if model is not None:
                            return Response({
                                "userType": model.__str__(),
                                # "username": data['username'],
                                "firstName": first_name,
                                # "session": newToken,
                            })

        if model is not None:
            # user_logged_in.send(sender=user.__class__, request=request, user=user)
            if program is None:
                program_id = ''
            else:
                program_id = dataProgram.data['program_id']
            return Response({
                "userType": model.__str__(),
                # "username": data['username'],
                "firstName": first_name,
                # "session": newToken,
                "program": program_id
            })


# /students/{program}
# [
#     {
#         "firstName": "string",
#         "lastName": "string",
#         "email": "string",
#         "company": "string",
#         "internship": "string",
#         "hours": 0,
#         "status": "string"
#     }
# ]
@api_view(['GET'])
def get_details_about_students_by_program(request, program):
    if request.method == 'GET':
        details = []
        student_and_program = StudentAndProgram.objects.all()
        student_and_program = student_and_program.filter(program_id=program)
        # print("1. student_and_program: ", student_and_program)
        student_and_program_serializer = StudentAndProgramSerializers(student_and_program, many=True)
        student_and_program_serializer = list(student_and_program_serializer.data)
        # print("2. student_and_program_serializer: ", student_and_program_serializer)
        for student in student_and_program_serializer:
            student_id = student['student_id']
            program_id = student['program_id']
            users = User.objects.all()
            user = users.filter(id=student_id)
            # print(user)
            user_serializer = UserSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            # print("user_serializer: ", user_serializer)
            first_name = user_serializer['first_name']
            last_name = user_serializer['last_name']
            email = user_serializer['email']
            students = Student.objects.all()
            student = students.filter(user_id=student_id)
            student_serializer = StudentSerializer(student, many=True)
            student_serializer = list(student_serializer.data)
            student_serializer = student_serializer[0]
            status = student_serializer['status']
            if status == student_status[2]:
                student_detail = {
                            "firstName": first_name,
                            "lastName": last_name,
                            "email": email,
                            "company": "empty-not implement",
                            "internship": "empty-not implement",
                            "hours": 0,
                            "status": status
                    }
            else:
                student_detail = {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email,
                    "status": status
                }
            details.append(student_detail)

        return Response(details)

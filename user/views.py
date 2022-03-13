# import tables
from django.shortcuts import render
from django.contrib.sessions.backends import db
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out

from program.models import StudentAndProgram, CompanyMentorAndProgram, CompanyRepresentativeAndProgram, \
    ProgramManagerAndProgram, ProgramCoordinatorAndProgram
from program.serializers import StudentAndProgramSerializers, CompanyMentorAndProgramSerializers, \
    CompanyRepresentativeAndProgramSerializers, ProgramManagerAndProgramSerializers, \
    ProgramCoordinatorAndProgramSerializers
from .models import Company, ProgramManager, Student, CompanyMentor, CompanyRepresentative, ProgramCoordinator, \
    SystemManager
# from .serializer import CompanyRepresentativeSerializer

from rest_framework.response import Response
import help_fanctions

from .serializer import CompanySerializer, UserDetailsSerializer, UserSerializer


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


#GET /users/details/{username}:
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

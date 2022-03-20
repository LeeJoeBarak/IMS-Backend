import tables
from django.contrib.sessions.backends import db
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from program.models import Program
from user.models import Company, CompanyRepresentative
from user.serializer import UserDetailsSerializer, CompanyRepresentativeSerializer
from .serializers import InternshipsSerializer, CreateInternshipSerializer
# from .serializers import InternshipsSerializer, NewInternshipSerializer, InternshipsPrioritiesByCandidateSerializer
from .models import Internship, Priority
from rest_framework.response import Response
from knox.models import AuthToken

import help_fanctions
from rest_framework import generics, permissions


class InternshipsView(viewsets.ModelViewSet):
    serializer_class = InternshipsSerializer
    queryset = Internship.objects.all()


# GET /internships/{program}
@api_view(['GET'])
def get_internships_by_program(request, program):
    if request.method == 'GET':
        internships = Internship.objects.all()
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

    def post(self, request, *args, **kwargs):
        # create internship:
        # print('1. request.data: ',request.data)
        program = Program.objects.filter(pk=request.data['program'])
        # print('2. program: ', program[0])
        company = Company.objects.filter(pk=request.data['company'])
        # print('3. company: ', company[0])
        internshipName = Internship.objects.filter(pk=request.data['internshipName'])
        # print('4. internshipName: ', internshipName)
        if program is None or company is None or len(internshipName) != 0:
            return Response('Invalid program / company / internship name supplied already exists',
                            status.HTTP_400_BAD_REQUEST)

        program_id = program[0]
        companyName_id = company[0]
        internship = Internship.objects.create(
            program=program_id,
            internshipName=request.data['internshipName'],
            companyName=companyName_id,
            about=request.data['about'],
            requirements=request.data['requirements']
        )
        # print('5. internship: ', internship)

        return Response(
            content_type='successful create a internship request', status=status.HTTP_201_CREATED)


# class PostCreateInternshipDetailsByProgramManager(generics.GenericAPIView):
#     authentication_classes = []
#     permission_classes = []
#     serializer_class = CreateInternshipSerializer
#
#     def post(self, request, *args, **kwargs):
#         # create internship:
#         # print('1. request.data: ',request.data)
#         program = Program.objects.filter(pk=request.data['program'])
#         # print('2. program: ', program[0])
#         company = Company.objects.filter(pk=request.data['company'])
#         # print('3. company: ', company[0])
#         internshipName = InternshipDetails.objects.filter(pk=request.data['internshipName'])
#         # print('4. internshipName: ', internshipName)
#         if program is None or company is None or len(internshipName) != 0:
#             return Response('Invalid program / company / internship name supplied already exists',
#                             status.HTTP_400_BAD_REQUEST)
#
#         program_id = program[0]
#         companyName_id = company[0]
#         internship = InternshipDetails.objects.create(
#             program=program_id,
#             internshipName=request.data['internshipName'],
#             companyName=companyName_id,
#             about=request.data['about'],
#             requirements=request.data['requirements']
#         )
#         # print('5. internship: ', internship)
#
#         return Response(
#             content_type='successful create a internship request', status=status.HTTP_201_CREATED)


# POST /companyRep/createInternship
class PostCreateInternshipByCompanyRep(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CreateInternshipSerializer

    def post(self, request, *args, **kwargs):
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
        try:
            program = Program.objects.filter(pk=request.data['program'])
            # print('4. program: ', program[0])
            company = Company.objects.filter(pk=company)
            # print('5. company: ', company[0])
            internshipName = Internship.objects.filter(pk=request.data['internshipName'])
            # print('4. internshipName: ', internshipName)
        except:
            return Response('Invalid program / company / internship name supplied already exists',
                            status.HTTP_400_BAD_REQUEST)

        if len(program) == 0 or len(company) == 0 or len(internshipName) != 0:
            return Response('Invalid program / company / internship name supplied already exists',
                            status.HTTP_400_BAD_REQUEST)

        program_id = program[0]
        companyName_id = company[0]
        internship = Internship.objects.create(
            program=program_id,
            internshipName=request.data['internshipName'],
            companyName=companyName_id,
            about=request.data['about'],
            requirements=request.data['requirements']
        )
        # print('5. internship: ', internship)

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

    def post(self, request, *args, **kwargs):
        internshipName_array = []

        try:
            users = User.objects.all()
            user = users.filter(username=request.data['username'])
            # print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            Student_id = user_serializer['id']
            # print('1. Student_id: ', Student_id)
            for internship in request.data['priorities']:
                internship_obj = Internship.objects.filter(pk=internship['internshipName'])
                print('internship_obj: ', internship_obj)
                internship_serializer = InternshipsSerializer(internship_obj, many=True)
                internship_serializer = internship_serializer[0]
                internship_id = internship_serializer[0]
                internshipName_array.append(internship_id)
                print('2. internship_id: ', internship_id)

        except:
            return Response('Invalid username supplied (not exist)', status.HTTP_400_BAD_REQUEST)

        for i, val in enumerate(internshipName_array):
            priority = Priority.objects.create(
                internship_id=internship_id,
                Student_id=Student_id,
                student_priority_number=request.data['internshipName'],
            )

        return Response(
            content_type='successful saved priorities', status=status.HTTP_201_CREATED)

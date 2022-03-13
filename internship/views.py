import tables
from django.contrib.sessions.backends import db
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status

from program.models import Program
from user.models import Company
from .serializers import InternshipsSerializer, CreateInternshipSerializer
# from .serializers import InternshipsSerializer, NewInternshipSerializer, InternshipsPrioritiesByCandidateSerializer
from .models import Internship
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
            return Response('Invalid program / company / internship name supplied already exists', status.HTTP_400_BAD_REQUEST)

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








        # POST /companyRep/createInternship
        # {
        #     "program": "string",
        #     "internshipName": "string",
        #     "about": "string",
        #     "requirements": "string"
        # }
        # class PostCreateInternshipByCompanyRep(generics.GenericAPIView):
        #     # authentication_classes = []
        #     # permission_classes = []
        #     # serializer_class = CreateProgramSerializer
        #
        #     def post(self, request, *args, **kwargs):
        #         # id = "SELECT user_id from main.knox_authtoken where token_key = '7bdcac92'"
        #         # # print(': ', companyRep/createInternship)
        #         lToken = '7bdcac92'
        #         q = AuthToken.objects.raw('SELECT user_id from main.knox_authtoken where token_key = %s', [lToken])
        #         print('q: ', q)
        # # create program:
        # serializer = self.get_serializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response('A program with the same name already exists', status.HTTP_400_BAD_REQUEST)
        #
        # # check if manager exist:
        # programManager = ProgramManager.objects.filter(pk=request.data['programManager'])
        # if len(programManager) == 0:
        #     return Response('Invalid program manager supplied (not exist)', status.HTTP_404_NOT_FOUND)
        #
        # program = serializer.save()
        #
        # programManager_program = ProgramManagerAndProgram.objects.create(
        #     program_id=ProgramNameSerializer(program, context=self.get_serializer_context()).data['program'],
        #     programManager_id=request.data['programManager'])
        # programManager_program.save()

        return Response(
            content_type='successful open a program',
            status=status.HTTP_201_CREATED
        )

# /candidate/internshipsPriorities:
# def set_internships_priorities_by_candidate(request):
#     if request.method == 'POST':
#         serializer = InternshipsPrioritiesByCandidateSerializer(data=request.data)
#
#         if serializer.is_valid():
#             print(serializer.data)
#             # serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def create_internship(request):
#     """company representative creates an internship offered by his company"""
#     #todo validate that the internship doesn't exist in system already
#     if request.method == "POST":
#         companyRepresentative_id = request.POST.get('username')
#         companyName = request.POST.get('companyName')
#         internshipName = request.POST.get('internshipName')
#         about = request.POST.get('about')
#         requirements = request.POST.get('requirments') #DON'T fix the typo (i.e. don't add 'e' after 'r')
#         mentor = request.POST.get('mentor')
#
#         #todo Validate username. If wrong username -> return 401 invalid username
#
#         data = {
#             companyRepresentative= companyRepresentative,
#             'companyName': companyName,
#             'internshipName': internshipName,
#             'about': about,
#             'requirements': requirments,
#             'mentor': mentor
#             'program': program
#         }
#
#         db, client = utils.get_db_handle()
#         internshipsColl = utils.get_collection_handle(db, "Internships")
#         res = internshipsColl.insert_one(data)
#         print("successful insert")
#         print(res.inserted_id)
#         return HttpResponse(200, 'internship created successfully')
#     return HttpResponse("request method wasn't POST")

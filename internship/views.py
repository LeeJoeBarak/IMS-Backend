import tables
from django.contrib.sessions.backends import db
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import InternshipsSerializer
# from .serializers import InternshipsSerializer, NewInternshipSerializer, InternshipsPrioritiesByCandidateSerializer
from .models import Internship
from rest_framework.response import Response
import help_fanctions


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


# GET /prioritiesAmount/{program}

# post /companyRep/createInternship:
# "username": "string",
# "companyName": "string",
# "internshipName": "string",
# "about": "string",
# "requirments": "string",
# "mentor": "string"
# @api_view(['POST'])
# def create_internship(request):
#     if request.method == 'POST':
#         serializer = NewInternshipSerializer(data=request.data)
#
#         if serializer.is_valid():
#             print(serializer.data)
#             # serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

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
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
from .models import Company, ProgramManager
# from .serializer import CompanyRepresentativeSerializer

from rest_framework.response import Response
import help_fanctions

from .serializer import CompanySerializer, UserDetailsSerializer


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

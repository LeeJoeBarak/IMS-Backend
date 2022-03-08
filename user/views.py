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

from .models import Company
# from .serializer import CompanyRepresentativeSerializer

from rest_framework.response import Response
import help_fanctions


from .serializer import CompanySerializer

# GET /companies
@api_view(['GET'])
def get_companies_list(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        companies_serializer = CompanySerializer(companies, many=True)
        return JsonResponse(companies_serializer.data, safe=False)


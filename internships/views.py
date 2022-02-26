import tables
from django.contrib.sessions.backends import db
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import InternshipsSerializer,NewInternshipSerializer
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

#post /companyRep/createInternship:
# "username": "string",
# "companyName": "string",
# "internshipName": "string",
# "about": "string",
# "requirments": "string",
# "mentor": "string"
@api_view(['POST'])
def create_internship(request):
    if request.method == 'POST':
        serializer = NewInternshipSerializer(data=request.data)

        if serializer.is_valid():
            print(serializer.data)
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

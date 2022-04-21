from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
# from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.status import HTTP_404_NOT_FOUND

from internship.models import InternshipDetails, Priority
from internship.serializers import InternshipsFullSerializer, InternshipsPrioritiesByCandidateSerializer
from profile_user.models import StudentProfile
from profile_user.serializers import StudentProfileSerializer
from program.models import Program, StudentAndProgram
from program.serializers import ProgramNameSerializer, StudentAndProgramSerializers
from user.models import Company, CompanyRepresentative, Student, CompanyMentor
from user.serializer import UserDetailsSerializer, CompanyRepresentativeSerializer, CompanySerializer, \
    UserSerializer, StudentSerializer
from rest_framework.response import Response
# from knox.models import AuthToken

import help_fanctions
from rest_framework import generics


# /student/profile/{username}:
# {
#     "username": "string",
#     "birthdate": "string",
#     "gitLink": "string",
#     "linkedinLink": "string",
#     "picture": "string",
#     "address": "string",
#     "phoneNumber": "string",
#     "cv": "string",
#     "gradesSheet": "string"
# }
@api_view(['GET'])
def get_student_profile(request, username):
    if request.method == 'GET':
        students_details = []
        try:
            # check if the username is of a real CompanyRepresentative
            users = User.objects.all()
            user = users.filter(username=username)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            student_id = user_serializer['id']
            # print("1. companyRep_id: ", student_id)
            # check if the user is a student:
            student = Student.objects.filter(user_id=student_id)
            # print("2. student: ", student)

            # print("2. student: ", student)
            student_profile = StudentProfile.objects.filter(student_id=student_id)
            # print("3. student_profile: ", student_profile)
            student_profile_serializer = StudentProfileSerializer(student_profile, many=True)
            student_profile_serializer = list(student_profile_serializer.data)
            student_profile_serializer = student_profile_serializer[0]
            # print("3. student_profile_serializer: ", student_profile_serializer)
        except:
            return Response('Invalid username supplied', status=status.HTTP_401_UNAUTHORIZED)

        student_details = {
            "username": username,
            "birthdate": student_profile_serializer['birthdate'],
            "gitLink": student_profile_serializer['gitLink'],
            "linkedinLink": student_profile_serializer['linkedinLink'],
            "picture": student_profile_serializer['picture'],
            "address": student_profile_serializer['address'],
            "phoneNumber": student_profile_serializer['phone_number'],
            "cv": student_profile_serializer['cv'],
            "gradesSheet": student_profile_serializer['gradesSheet']
        }
        return JsonResponse(student_details, safe=False)


# /student/createProfile:
# {
#     "username": "string",
#     "birthdate": "string",
#     "gitLink": "string",
#     "linkedinLink": "string",
#     "picture": "string",
#     "address": "string",
#     "phoneNumber": "string",
#     "cv": "string",
#     "gradesSheet": "string"
# }
class PostCreateStudentProfile(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            users = User.objects.all()
            user = users.filter(username=request.data['username'])
            if not user.exists():
                return Response('Invalid companyName\internshipName\studentName supplied', status=HTTP_404_NOT_FOUND)
            print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            student_id = user_serializer['id']
            print('2. student_id: ', student_id)
            student = Student.objects.filter(user_id=student_id)
            student_serializer = StudentSerializer(student, many=True)
            student_serializer = list(student_serializer.data)
            student_serializer = student_serializer[0]
        except:
            return Response('Invalid username', status.HTTP_401_UNAUTHORIZED)
        try:
            student_profile = StudentProfile.objects.filter(student_id=student_id)
        except:
            return Response('Already profile exist', status.HTTP_400_BAD_REQUEST)
        print('3. gradesSheet: ', request.data['gradesSheet'])
        student_profile = StudentProfile.objects.create(
            phone_number=request.data['phoneNumber'],
            birthdate=request.data['birthdate'],
            gitLink=request.data['gitLink'],
            linkedinLink=request.data['linkedinLink'],
            address=request.data['address'],
            picture=request.data['picture'],
            cv=request.data['cv'],
            gradesSheet=request.data['gradesSheet'],
            student_id=student_id)
        student_profile.save()

        return Response(content_type='successful create a profile', status=status.HTTP_200_OK)

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.status import HTTP_404_NOT_FOUND
from profile_user.models import StudentProfile, CompanyProfile
from profile_user.serializers import StudentProfileSerializer, CompanyProfileSerializer
from user.models import Company, Student
from user.serializer import UserDetailsSerializer, StudentSerializer
from rest_framework.response import Response
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
        try:
            # check if the username is of a real CompanyRepresentative
            users = User.objects.all()
            user = users.filter(username=username)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            student_id = user_serializer['id']
            # check if the user is a student:
            Student.objects.filter(user_id=student_id)

            student_profile = StudentProfile.objects.filter(student_id=student_id)
            student_profile_serializer = StudentProfileSerializer(student_profile, many=True)
            student_profile_serializer = list(student_profile_serializer.data)
            student_profile_serializer = student_profile_serializer[0]
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
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            student_id = user_serializer['id']
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


# POST /companyRep/createCompanyProfile:
# {
#     "companyName": "string",
#     "yearEstablish": 0,
#     "workersAmount": 0,
#     "location": "string",
#     "about": "string",
# "linkedinLink": "string",
# }
class PostCreateCompanyProfile(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            company_name = request.data['companyName']
            company = Company.objects.filter(pk=company_name)
        except:
            return Response('Invalid company supplied', status.HTTP_401_UNAUTHORIZED)
        try:
            company_profile = CompanyProfile.objects.filter(pk=company_name)
        except:
            return Response('Already profile exist', status.HTTP_400_BAD_REQUEST)
        # create company:
        company_profile = CompanyProfile.objects.create(
            companyName_id=company,
            yearEstablish=request.data['yearEstablish'],
            workersAmount=request.data['workersAmount'],
            linkedinLink=request.data['linkedinLink'],
            location=request.data['location'],
            about=request.data['about'])
        company_profile.save()

        return Response(content_type='successful create a profile to the company', status=status.HTTP_200_OK)


# GET /company/{companyName}
# {
#     "companyName": "string",
#     "yearEstablish": 0,
#     "workersAmount": 0,
#     "location": "string",
#     "about": "string",
#     "linkedinLink": "string"
# }
@api_view(['GET'])
def get_company_profile(request, companyName):
    if request.method == 'GET':
        try:
            company = Company.objects.filter(pk=companyName)
            company_profile = CompanyProfile.objects.filter(companyName_id=company[0])
            company_profile_serializer = CompanyProfileSerializer(company_profile, many=True)
            company_profile_serializer = list(company_profile_serializer.data)
            company_profile_serializer = company_profile_serializer[0]
        except:
            return Response('Invalid company name supplied', status=status.HTTP_401_UNAUTHORIZED)

        company_details = {
            "companyName": companyName,
            "yearEstablish": company_profile_serializer['yearEstablish'],
            "workersAmount": company_profile_serializer['workersAmount'],
            "linkedinLink": company_profile_serializer['linkedinLink'],
            "location": company_profile_serializer['location'],
            "about": company_profile_serializer['about'],

        }
        return JsonResponse(company_details, safe=False)

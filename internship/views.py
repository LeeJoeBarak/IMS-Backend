# import tables
# from django.contrib.sessions.backends import db
from django.http import JsonResponse
# from django.shortcuts import render
# from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
# from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.status import HTTP_404_NOT_FOUND

from program.models import Program, StudentAndProgram
from program.serializers import ProgramNameSerializer, StudentAndProgramSerializers
from user.models import Company, CompanyRepresentative, Student
from user.serializer import UserDetailsSerializer, CompanyRepresentativeSerializer, CompanySerializer, \
    UserSerializer, StudentSerializer
from .serializers import InternshipsSerializer, CreateInternshipSerializer, InternshipIdSerializer, \
    InternshipsPrioritiesByCandidateSerializer, HoursReportSerializer
# from .serializers import InternshipsSerializer, NewInternshipSerializer, InternshipsPrioritiesByCandidateSerializer
from .models import Priority, InternshipDetails, AssignmentIntern, HoursReport
from rest_framework.response import Response
# from knox.models import AuthToken

import help_fanctions
from rest_framework import generics


class InternshipsView(viewsets.ModelViewSet):
    serializer_class = InternshipsSerializer
    queryset = InternshipDetails.objects.all()


# GET /internships/{program}
@api_view(['GET'])
def get_internships_by_program(request, program):
    if request.method == 'GET':
        internships = InternshipDetails.objects.all()
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


# GET /programManager/{program}/{companyName}/{internshipName}/nominees:
# [
#     {
#         "username": "string",
#         "firstName": "string",
#         "lastName": "string",
#         "status": "string"
#     }
# ]
@api_view(['GET'])
def get_nominees(request, program, companyName, internshipName):
    if request.method == 'GET':
        student_details = []
        internship_obj = InternshipDetails.objects.filter(internshipName=internshipName,
                                                          program_id=program,
                                                          companyName_id=companyName)
        if not internship_obj.exists():
            return Response('company/internship not found', status=HTTP_404_NOT_FOUND)
        internship_serializer = InternshipIdSerializer(internship_obj, many=True)
        # print('5. internship_serializer: ', internship_serializer.data)
        internship_serializer = list(internship_serializer.data)
        # print('6. internship_serializer: ', internship_serializer)
        internship_serializer = internship_serializer[0]
        # print('7. internship_serializer: ', internship_serializer)
        internship_id = internship_serializer['id']
        nominees = Priority.objects.filter(internship_id=internship_id)
        # InternshipsPrioritiesByCandidateSerializer
        nominees_serializer = InternshipsPrioritiesByCandidateSerializer(nominees, many=True)
        nominees_serializer = list(nominees_serializer.data)
        # program_id = program_serializer['program_id']
        # print('1. nominees_serializer: ', nominees_serializer)
        for nominee in nominees_serializer:
            # print('2. nominee: ', nominee)
            users = User.objects.all()
            user = users.filter(id=nominee['Student_id'])
            # print("3. user: ", user)
            user_serializer = UserSerializer(user, many=True)
            # print("3. user_serializer: ", user_serializer)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            username = user_serializer['username']
            firstName = user_serializer['first_name']
            lastName = user_serializer['last_name']
            # print('A. username: ', username)
            # print('B. firstName: ', firstName)
            # print('C. lastName: ', lastName)
            students = Student.objects.all()
            student = students.filter(user_id=nominee['Student_id'])
            student_serializer = StudentSerializer(student, many=True)
            student_serializer = list(student_serializer.data)
            student_serializer = student_serializer[0]
            if student_serializer["status"] == help_fanctions.student_status[1]:
                student_detail = {
                    "username": username,
                    "firstName": firstName,
                    "lastName": lastName,
                }
                student_details.append(student_detail)
        return JsonResponse(student_details, safe=False)


# assign to internship
# @api_view(['GET'])
# def get_nominees(request, program, companyName, internshipName):
#     if request.method == 'GET':
#         student_details = []
#         internship_obj = InternshipDetails.objects.filter(internshipName=internshipName,
#                                                           program_id=program,
#                                                           companyName_id=companyName)
#         if not internship_obj.exists():
#             return Response('company/internship not found', status=HTTP_404_NOT_FOUND)
#         internship_serializer = InternshipIdSerializer(internship_obj, many=True)
#         # print('5. internship_serializer: ', internship_serializer.data)
#         internship_serializer = list(internship_serializer.data)
#         # print('6. internship_serializer: ', internship_serializer)
#         internship_serializer = internship_serializer[0]
#         # print('7. internship_serializer: ', internship_serializer)
#         internship_id = internship_serializer['id']
#         nominees = Priority.objects.filter(internship_id=internship_id)
#         # InternshipsPrioritiesByCandidateSerializer
#         nominees_serializer = InternshipsPrioritiesByCandidateSerializer(nominees, many=True)
#         nominees_serializer = list(nominees_serializer.data)
#         # program_id = program_serializer['program_id']
#         # print('1. nominees_serializer: ', nominees_serializer)
#         for nominee in nominees_serializer:
#             # print('2. nominee: ', nominee)
#             users = User.objects.all()
#             user = users.filter(id=nominee['Student_id'])
#             # print("3. user: ", user)
#             user_serializer = UserSerializer(user, many=True)
#             # print("3. user_serializer: ", user_serializer)
#             user_serializer = list(user_serializer.data)
#             user_serializer = user_serializer[0]
#             username = user_serializer['username']
#             firstName = user_serializer['first_name']
#             lastName = user_serializer['last_name']
#             # print('A. username: ', username)
#             # print('B. firstName: ', firstName)
#             # print('C. lastName: ', lastName)
#             students = Student.objects.all()
#             student = students.filter(user_id=nominee['Student_id'])
#             student_serializer = StudentSerializer(student, many=True)
#             student_serializer = list(student_serializer.data)
#             student_serializer = student_serializer[0]
#             if student_serializer["status"] == help_fanctions.student_status[1]:
#                 student_detail = {
#                     "username": username,
#                     "firstName": firstName,
#                     "lastName": lastName,
#                 }
#                 student_details.append(student_detail)
#         return JsonResponse(student_details, safe=False)


# GET /intern/getHours/{username}:
# [
#     {
#         "date": "string",
#         "startTime": "string",
#         "endTime": "string",
#         "approved": true
#     }
# ]
@api_view(['GET'])
def get_intern_hours(request, username):
    if request.method == 'GET':
        hours_details = []
        try:
            users = User.objects.all()
            user = users.filter(username=username)
            # if not user.exists():
            #     return Response('User not found - user', status=status.HTTP_404_NOT_FOUND)
            # print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            Student_id = user_serializer['id']
            # check if the user is a student:
            student = Student.objects.get(user_id=Student_id)
            # print("2. student: ", student)
        except:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        hours = HoursReport.objects.filter(student_id=Student_id)
        hours_serializer = HoursReportSerializer(hours, many=True)
        hours_serializer = list(hours_serializer.data)
        for hour in hours_serializer:
            hour_details = {
                "date": hour['date'],
                "startTime": hour['startTime'],
                "endTime": hour['endTime'],
                "approved": hour['approved']
            }
            hours_details.append(hour_details)
        return JsonResponse(hours_details, safe=False)


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

    def post(self, request):
        # create internship:
        # print('1. request.data: ', request.data)
        program = Program.objects.filter(pk=request.data['program'])
        # print('2. program: ', program[0])
        company = Company.objects.filter(pk=request.data['company'])
        # print('3. company: ', company[0])
        internshipName = InternshipDetails.objects.filter(internshipName=request.data['internshipName'],
                                                          program_id=program[0], companyName_id=company[0])
        # print('4. internshipName: ', internshipName)
        if program is None or company is None or len(internshipName) != 0:
            return Response('Invalid program / company / internship name supplied already exists',
                            status.HTTP_400_BAD_REQUEST)
        # print('5. Start create: ')
        program_id = program[0]
        companyName_id = company[0]
        internship = InternshipDetails.objects.create(
            program_id=ProgramNameSerializer(program_id, context=self.get_serializer_context()).data['program'],
            internshipName=request.data['internshipName'],
            companyName_id=CompanySerializer(companyName_id, context=self.get_serializer_context()).data['companyName'],
            about=request.data['about'],
            requirements=request.data['requirements']
        )
        # print('6. internship: ', internship)

        return Response(
            content_type='successful create a internship request', status=status.HTTP_201_CREATED)


# POST /companyRep/createInternship
class PostCreateInternshipByCompanyRep(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CreateInternshipSerializer

    def post(self, request):
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
            internshipName = InternshipDetails.objects.filter(internshipName=request.data['internshipName'],
                                                              program_id=program[0], companyName_id=company[0])
            # print('4. internshipName: ', internshipName)
        except:
            return Response('Invalid program / company / internship name supplied already exists',
                            status.HTTP_400_BAD_REQUEST)

        if len(program) == 0 or len(company) == 0 or len(internshipName) != 0:
            return Response('Invalid program / company / internship name supplied already exists',
                            status.HTTP_400_BAD_REQUEST)

        program_id = program[0]
        companyName_id = company[0]
        internship = InternshipDetails.objects.create(
            program_id=ProgramNameSerializer(program_id, context=self.get_serializer_context()).data['program'],
            internshipName=request.data['internshipName'],
            companyName_id=CompanySerializer(companyName_id, context=self.get_serializer_context()).data['companyName'],
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

    def post(self, request):
        internshipName_array = []

        try:
            users = User.objects.all()
            user = users.filter(username=request.data['username'])
            # print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            Student_id = user_serializer['id']
            # print('2. Student_id: ', Student_id)
            program = StudentAndProgram.objects.filter(student_id=Student_id)
            program_serializer = StudentAndProgramSerializers(program, many=True)
            program_serializer = list(program_serializer.data)
            program_serializer = program_serializer[0]
            program_id = program_serializer['program_id']
            # print('3. program_id: ', program_id)
            for internship in request.data['priorities']:
                # print('3. details: ', internship['internshipName'], program_id, internship['companyName'])
                internship_obj = InternshipDetails.objects.filter(internshipName=internship['internshipName'],
                                                                  program_id=program_id,
                                                                  companyName_id=internship['companyName'])
                # print('4. internship_obj: ', internship_obj)
                internship_serializer = InternshipIdSerializer(internship_obj, many=True)
                # print('5. internship_serializer: ', internship_serializer.data)
                internship_serializer = list(internship_serializer.data)
                # print('6. internship_serializer: ', internship_serializer)
                internship_serializer = internship_serializer[0]
                # print('7. internship_serializer: ', internship_serializer)
                internship_id = internship_serializer['id']
                # print('8. internship_obj: ', internship_obj)
                internshipName_array.append(internship_id)
                # print('9. internship_id: ', internship_id)

        except:
            return Response('Invalid username supplied (not exist)', status.HTTP_400_BAD_REQUEST)

        for i, val in enumerate(internshipName_array):
            priority = Priority.objects.create(
                internship_id=val,
                Student_id=Student_id,
                student_priority_number=i + 1,
            )

        return Response(content_type='successful saved priorities', status=status.HTTP_200_OK)


# POST /assignIntern:
# {
#     "companyName": "string",
#     "internshipName": "string",
#     "username": "string"
# }

class AssignInternToInternship(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        users = User.objects.all()
        user = users.filter(username=request.data['username'])
        if not user.exists():
            return Response('Invalid companyName\internshipName\studentName supplied', status=HTTP_404_NOT_FOUND)
        # print("1. user: ", user)
        user_serializer = UserDetailsSerializer(user, many=True)
        user_serializer = list(user_serializer.data)
        user_serializer = user_serializer[0]
        Student_id = user_serializer['id']
        # print('2. Student_id: ', Student_id)
        program = StudentAndProgram.objects.filter(student_id=Student_id)
        if not program.exists():
            return Response('Invalid companyName\internshipName\studentName supplied', status=HTTP_404_NOT_FOUND)
        program_serializer = StudentAndProgramSerializers(program, many=True)
        program_serializer = list(program_serializer.data)
        program_serializer = program_serializer[0]
        program_id = program_serializer['program_id']
        # print('3. program_id: ', program_id)
        internship_obj = InternshipDetails.objects.filter(internshipName=request.data['internshipName'],
                                                          program_id=program_id,
                                                          companyName_id=request.data['companyName'])
        if not internship_obj.exists():
            return Response('Invalid companyName\internshipName\studentName supplied', status=HTTP_404_NOT_FOUND)
        internship_serializer = InternshipIdSerializer(internship_obj, many=True)
        # print('5. internship_serializer: ', internship_serializer.data)
        internship_serializer = list(internship_serializer.data)
        # print('6. internship_serializer: ', internship_serializer)
        internship_serializer = internship_serializer[0]
        # print('7. internship_serializer: ', internship_serializer)
        internship_id = internship_serializer['id']

        # Assign intern:
        assignIntern = AssignmentIntern.objects.filter(student_id=Student_id, internship_id=internship_id, )
        if assignIntern.exists():
            return Response('The assignment intern already exist', status=HTTP_404_NOT_FOUND)
        assignIntern = AssignmentIntern.objects.create(
            student_id=Student_id,
            internship_id=internship_id,
        )

        # update student status:
        student = Student.objects.get(user_id=Student_id)
        student.status = help_fanctions.student_status[2]
        student.save()

        # update internship isAssign:
        internship = InternshipDetails.objects.get(id=internship_id)
        # print('7. internship: ', internship)
        # print('6. internship.isAssign: ', internship.isAssign)
        internship.isAssign = True
        # print('7. After internship.isAssign: ', internship.isAssign)
        internship.save()

        return Response(
            content_type='successful set the student to the intern', status=status.HTTP_201_CREATED)


# POST /intern/hoursReport:
# {
#     "username": "string",
#     "hours": [
#         {
#             "date": "string",
#             "startTime": "string",
#             "endTime": "string"
#         }
#     ]
# }
class HoursReportByIntern(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # print("request.data: ", request.data)
        # get student id:
        try:
            users = User.objects.all()
            user = users.filter(username=request.data['username'])
            if not user.exists():
                return Response('Invalid username supplied', status=status.HTTP_401_UNAUTHORIZED)
            # print("1. user: ", user)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            Student_id = user_serializer['id']
            # check if the user is a student:
            student = Student.objects.get(user_id=Student_id)
        except:
            return Response('Invalid username supplied', status=status.HTTP_401_UNAUTHORIZED)
        # print('2. Student_id: ', Student_id)
        # print('3. hours:' , request.data['hours'])
        # Report hour:
        for hour in request.data['hours']:
            l_hour = dict(hour)
            # print('3. hours:' , request.data['hours'])
            checkHoursReport = HoursReport.objects.filter(student_id=Student_id, date=l_hour['date'],
                                                          startTime=l_hour['startTime'],
                                                          endTime=l_hour['endTime'])
            if checkHoursReport.exists():
                continue
            hoursReport = HoursReport.objects.create(
                student_id=Student_id,
                date=l_hour['date'],
                startTime=l_hour['startTime'],
                endTime=l_hour['endTime'],
                totalTime=l_hour['totalTime']
            )
            # print('A. date: ', l_hour['date'])
            # print('B. startTime: ', l_hour['startTime'])
            # print('C. endTime: ', l_hour['endTime'])
            # print("3. hoursReport: ", hoursReport)

        return Response(
            content_type='successful add the hours', status=status.HTTP_200_OK)

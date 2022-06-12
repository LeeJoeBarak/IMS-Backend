from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.status import HTTP_404_NOT_FOUND

from help_fanctions import student_status
from internship.models import AssignmentIntern, InternshipDetails, HoursReport
from internship.serializers import AssignmentInternSerializer, InternshipsSerializer, \
    HoursReportTotalTimeSerializer
from program.models import StudentAndProgram, CompanyMentorAndProgram, CompanyRepresentativeAndProgram, \
    ProgramManagerAndProgram, ProgramCoordinatorAndProgram
from program.serializers import StudentAndProgramSerializers, CompanyMentorAndProgramSerializers, \
    CompanyRepresentativeAndProgramSerializers, ProgramManagerAndProgramSerializers, \
    ProgramCoordinatorAndProgramSerializers
from .models import Company, ProgramManager, Student, CompanyMentor, CompanyRepresentative, ProgramCoordinator, \
    SystemManager
from rest_framework.response import Response
from .serializer import UserDetailsSerializer, UserSerializer, StudentSerializer, MentorSerializer, \
    CompanyRepresentativeSerializer


# GET /companies
@api_view(['GET'])
def get_companies_list(request):
    if request.method == 'GET':
        companies_list = Company.objects.values_list('companyName', flat=True)
        companies_list = list(companies_list)
        return JsonResponse(companies_list, safe=False)


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


# GET /users/details/{username}:
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
        user_serializer = UserDetailsSerializer(user, many=True)
        user_serializer = list(user_serializer.data)
        user_serializer = user_serializer[0]
        first_name = user_serializer['first_name']
        user_id = user_serializer['id']
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
                            return Response({
                                "userType": model.__str__(),
                                # "username": data['username'],
                                "firstName": first_name,
                                # "session": newToken,
                            })

        if model is not None:
            if program is None:
                program_id = ''
            else:
                program_id = dataProgram.data['program_id']
            return Response({
                "userType": model.__str__(),
                "firstName": first_name,
                "program": program_id
            })


# /students/{program}
# [
#     {
#         "firstName": "string",
#         "lastName": "string",
#         "email": "string",
#         "company": "string",
#         "internship": "string",
#         "hours": 0,
#         "status": "string"
#     }
# ]
@api_view(['GET'])
def get_details_about_students_by_program(request, program):
    if request.method == 'GET':
        details = []
        student_and_program = StudentAndProgram.objects.all()
        student_and_program = student_and_program.filter(program_id=program)
        student_and_program_serializer = StudentAndProgramSerializers(student_and_program, many=True)
        student_and_program_serializer = list(student_and_program_serializer.data)
        for student in student_and_program_serializer:
            student_id = student['student_id']
            users = User.objects.all()
            user = users.filter(id=student_id)
            user_serializer = UserSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            first_name = user_serializer['first_name']
            last_name = user_serializer['last_name']
            email = user_serializer['email']
            students = Student.objects.all()
            student = students.filter(user_id=student_id)
            student_serializer = StudentSerializer(student, many=True)
            student_serializer = list(student_serializer.data)
            student_serializer = student_serializer[0]
            status = student_serializer['status']
            # print("1. student_id: ", student_id)

            if status == student_status[2]:
                internship = AssignmentIntern.objects.filter(student_id=student_id)
                internship_serializer = AssignmentInternSerializer(internship, many=True)
                # print("2. internship_serializer: ", internship_serializer.data)
                internship_serializer = list(internship_serializer.data)

                internship_serializer = internship_serializer[0]
                internship_id = internship_serializer['internship_id']

                internshipName = InternshipDetails.objects.filter(pk=internship_id)
                internshipName_serializer = InternshipsSerializer(internshipName, many=True)
                internshipName_serializer = list(internshipName_serializer.data)
                internshipName_serializer = internshipName_serializer[0]
                internshipName = internshipName_serializer['internshipName']
                companyName = internshipName_serializer['companyName']

                hours = HoursReport.objects.filter(student_id=student_id)
                hours_serializer = HoursReportTotalTimeSerializer(hours, many=True)
                hours_serializer = list(hours_serializer.data)
                totalSecs = 0
                for hour in hours_serializer:
                    tm = hour['totalTime']
                    timeParts = [int(s) for s in tm.split(':')]
                    totalSecs += (timeParts[0] * 60 + timeParts[1])
                hr, minute = divmod(totalSecs, 60)
                total_hours = "%d:%02d" % (hr, minute)

                student_detail = {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email,
                    "company": companyName,
                    "internship": internshipName,
                    "hours": total_hours,
                    "status": status
                }
            else:
                student_detail = {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email,
                    "status": status
                }
            details.append(student_detail)

        return Response(details)


# /mentors/{company}:
@api_view(['GET'])
def get_mentors_by_company(request, company):
    if request.method == 'GET':
        mentor_details = []
        Company.objects.filter(companyName=company)
        companyMentors_list = CompanyMentor.objects.filter(company_id=company)
        companyMentors_serializer = MentorSerializer(companyMentors_list, many=True)
        companyMentors_serializer = list(companyMentors_serializer.data)
        for mentor in companyMentors_serializer:
            users = User.objects.all()
            user = users.filter(pk=mentor['user_id'])
            user_serializer = UserSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            mentor_detail = {
                "firstName": user_serializer['first_name'],
                "lastName": user_serializer['last_name'],
                "username": user_serializer['username']
            }
            mentor_details.append(mentor_detail)

        return JsonResponse(mentor_details, safe=False)


# GET /mentors/{companyRep}:
# [
#     {
#         "username": "string",
#         "firstName": "string",
#         "lastName": "string"
#     }
# ]
@api_view(['GET'])
def get_mentors_by_companyRep(request, companyRep):
    if request.method == 'GET':
        try:
            # check if the username is of a real CompanyRepresentative
            users = User.objects.all()
            user = users.filter(username=companyRep)
            user_serializer = UserDetailsSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            companyRep_id = user_serializer['id']
            # check if the user is a mentor:
            companyRep = CompanyRepresentative.objects.filter(user_id=companyRep_id)
        except:
            return Response('companyRep not found', status=HTTP_404_NOT_FOUND)
        # get company's CompanyRepresentative:
        companyRepresentative = CompanyRepresentativeSerializer(companyRep, many=True)
        companyRepresentative = list(companyRepresentative.data)
        companyRepresentative = companyRepresentative[0]
        company = companyRepresentative['companyName']
        mentor_details = []
        Company.objects.filter(companyName=company)
        companyMentors_list = CompanyMentor.objects.filter(company_id=company)
        companyMentors_serializer = MentorSerializer(companyMentors_list, many=True)
        companyMentors_serializer = list(companyMentors_serializer.data)
        for mentor in companyMentors_serializer:
            users = User.objects.all()
            user = users.filter(pk=mentor['user_id'])
            user_serializer = UserSerializer(user, many=True)
            user_serializer = list(user_serializer.data)
            user_serializer = user_serializer[0]
            mentor_detail = {
                "firstName": user_serializer['first_name'],
                "lastName": user_serializer['last_name'],
                "username": user_serializer['username']
            }
            mentor_details.append(mentor_detail)

        return JsonResponse(mentor_details, safe=False)

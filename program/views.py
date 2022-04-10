from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
# from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User

from user.models import ProgramManager
from user.serializer import UserDetailsSerializer
from .serializers import PrioritiesAmountSerializer, HoursRequiredSerializer, ProgramNameSerializer, \
    CreateProgramSerializer, ProgramsSerializer, ProgramManagerAndProgramSerializers
from .models import Program, ProgramManagerAndProgram
from rest_framework.response import Response
from rest_framework import generics, permissions

import help_fanctions


class InternshipsView(viewsets.ModelViewSet):
    serializer_class = PrioritiesAmountSerializer
    queryset = Program.objects.all()


# GET /prioritiesAmount/{program}:
@api_view(['GET'])
def get_priorities_amount_by_program(request, program):
    if request.method == 'GET':
        programs = Program.objects.all()
        programs = programs.filter(program=program)

        if not programs.exists():
            return Response('program not found', status=status.HTTP_404_NOT_FOUND)

        program_serializer = PrioritiesAmountSerializer(programs, many=True)
        amount = list(program_serializer.data)
        amount = amount[0]
        # return JsonResponse(amount, safe=False)
        return JsonResponse(amount['prioritiesAmount'], safe=False)


# GET /hoursRequired/{program}:
@api_view(['GET'])
def get_hours_required_by_program(request, program):
    if request.method == 'GET':
        programs = Program.objects.all()
        programs = programs.filter(program=program)

        if not programs.exists():
            return Response('program not found', status=status.HTTP_404_NOT_FOUND)

        program_serializer = HoursRequiredSerializer(programs, many=True)
        amount = list(program_serializer.data)
        amount = amount[0]
        return JsonResponse(amount['hoursRequired'], safe=False)


# /admin/programs:
# [
#     {
#         "program": "string",
#         "year": 0,
#         "semester": "string",
#         "prioritiesAmount": 0,
#         "hoursRequired": 0,
#         "department": "string",
#         "programManager_first_name": "string",
#         "programManager_last_name": "string",
#         "active": true
#     }
# ]
@api_view(['GET'])
def get_programs(request):
    if request.method == 'GET':
        programs_details = []
        try:
            programs = Program.objects.all()
            if not programs.exists():
                return Response('program not found', status=status.HTTP_404_NOT_FOUND)
            program_serializer = ProgramsSerializer(programs, many=True)
            program_serializer = list(program_serializer.data)
            for program in program_serializer:
                programManagerAndProgram = ProgramManagerAndProgram.objects.all()
                if not programManagerAndProgram.exists():
                    return Response('ProgramManagerAndProgram not found', status=status.HTTP_404_NOT_FOUND)
                ProgramManagerAndProgram_serializer = ProgramManagerAndProgramSerializers(programManagerAndProgram,
                                                                                          many=True)
                ProgramManagerAndProgram_serializer = list(ProgramManagerAndProgram_serializer.data)
                programManager_list = list(ProgramManagerAndProgram_serializer)
                first_name = ''
                last_name = ''
                for programManager in programManager_list:
                    if programManager['program_id'] == program['program']:
                        programManager_id = programManager['programManager_id']
                        users = User.objects.all()
                        user = users.filter(pk=programManager_id)
                        user_serializer = UserDetailsSerializer(user, many=True)
                        user_serializer = list(user_serializer.data)
                        user_serializer = user_serializer[0]
                        first_name = user_serializer['first_name']
                        last_name = user_serializer['last_name']
                        break

                program_details = {
                    "program": program['program'],
                    "year": program['year'],
                    "semester": program['semester'],
                    "prioritiesAmount": program['prioritiesAmount'],
                    "hoursRequired": program['hoursRequired'],
                    "department": program['department'],
                    "active": program['status'],
                    "programManager_first_name": first_name,
                    "programManager_last_name": last_name,
                }
                programs_details.append(program_details)
        except:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(programs_details, safe=False, status=status.HTTP_200_OK)


# activePrograms:
@api_view(['GET'])
def get_active_program(request):
    if request.method == 'GET':
        program_list = Program.objects.values_list('program', flat=True).order_by('program').filter(status='True')
        program_list = list(program_list)
        return JsonResponse(program_list, safe=False)


# POST /admin/openProgram:
class PostCreateProgram(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CreateProgramSerializer

    def post(self, request, *args, **kwargs):
        # create program:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response('A program with the same name already exists', status.HTTP_400_BAD_REQUEST)

        # check if manager exist:
        programManager = ProgramManager.objects.filter(pk=request.data['programManager'])
        if len(programManager) == 0:
            return Response('Invalid program manager supplied (not exist)', status.HTTP_404_NOT_FOUND)

        program = serializer.save()

        programManager_program = ProgramManagerAndProgram.objects.create(
            program_id=ProgramNameSerializer(program, context=self.get_serializer_context()).data['program'],
            programManager_id=request.data['programManager'])
        programManager_program.save()

        return Response(
            content_type='successful open a program',
            status=status.HTTP_201_CREATED
        )

# get_detail_about_program(detail = 'hoursRequired')

# @api_view(['GET'])
# def get_detail_about_program(request, program, detail):
#     if request.method == 'GET':
#         programs = Program.objects.all()
#         programs = programs.filter(program=program)
#
#         if not programs.exists():
#             return Response('program not found', status=status.HTTP_404_NOT_FOUND)
#
#         program_serializer = ProgramsSerializer(programs, many=True)
#         data = list(program_serializer.data)
#         data = data[0]
#         return JsonResponse(data[detail], safe=False)

from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status

from user.models import ProgramManager
from .serializers import PrioritiesAmountSerializer, HoursRequiredSerializer, ProgramNameSerializer, \
    CreateProgramSerializer
from .models import Program, ProgramManagerAndProgram
from rest_framework.response import Response
from rest_framework import generics, permissions

import help_fanctions


class InternshipsView(viewsets.ModelViewSet):
    serializer_class = PrioritiesAmountSerializer
    queryset = Program.objects.all()


# GET  /prioritiesAmount/{program}:
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


# GET  /hoursRequired/{program}:
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


# activePrograms:
@api_view(['GET'])
def get_active_program(request):
    if request.method == 'GET':
        # programs = Program.objects.all()
        # print("programs: ", programs)
        # programs = programs.filter(status="True")
        #
        # # if not programs.exists():
        # #     return Response('program not found', status=status.HTTP_404_NOT_FOUND)
        # program_serializer = ProgramNameSerializer(programs, many=True)
        # print("program_serializer.data: ",program_serializer.data)
        # # amount = list(program_serializer.data)
        # # amount = amount[0]
        program_list = Program.objects.values_list('program', flat=True).order_by('program').filter(status='True')
        # program = Program.objects.filter(program=request.data['program'], status='True')
        program_list = list(program_list)
        # print("program_list:", program_list)
        # return JsonResponse(program_serializer.data, safe=False)
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

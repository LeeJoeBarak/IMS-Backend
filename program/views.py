from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PrioritiesAmountSerializer,HoursRequiredSerializer
from .models import Program
from rest_framework.response import Response
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

from rest_framework import serializers

import internship
from .models import InternshipDetails, Priority, HoursReport


class InternshipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipDetails
        fields = ('program', 'companyName', 'internshipName', 'about', 'requirements')

        # "companyName": "string",
        # "internshipName": "string",
        # "about": "string",
        # "requirments": "string"


class InternshipIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipDetails
        fields = ('id', 'internshipName')


class CreateInternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipDetails
        fields = ('id', 'program_id', 'internshipName', 'companyName_id', 'about', 'requirements', 'quantity')


# class CreateInternshipSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InternshipDetails
#         fields = ('program_id', 'internshipName', 'companyName_id', 'about', 'requirements')


# "username": "string",
# "companyName": "string",
# "internshipName": "string",
# "about": "string",
# "requirments": "string",
# "mentor": "string"

class InternshipsPrioritiesByCandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ('Student_id', 'student_priority_number', 'internship_id')


# HoursReport
class HoursReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoursReport
        fields = ('student_id', 'date', 'startTime', 'endTime', 'approved', 'totalTime')

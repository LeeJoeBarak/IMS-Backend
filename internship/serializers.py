from rest_framework import serializers

import internship
from .models import Internship


class InternshipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = ('program', 'companyName', 'internshipName', 'about', 'requirements')

        # "companyName": "string",
        # "internshipName": "string",
        # "about": "string",
        # "requirments": "string"


class CreateInternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = ('program_id', 'internshipName', 'companyName_id', 'about', 'requirements')

        # def create(self, validated_data):
        #     internship = Internship.objects.create(
        #         internshipName=validated_data['internshipName'],
        #         program_id=validated_data['program'],
        #         companyName_id=validated_data['company'],
        #         about=validated_data['about'],
        #         requirements=validated_data['requirements']
        #     )
        #     return internship

# "username": "string",
# "companyName": "string",
# "internshipName": "string",
# "about": "string",
# "requirments": "string",
# "mentor": "string"

# class InternshipsPrioritiesByCandidateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Priority
#         fields = ('Student', 'internship')

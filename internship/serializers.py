from rest_framework import serializers
from .models import Internship


class InternshipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = ('program', 'companyName', 'internshipName', 'about', 'requirements')

        # "companyName": "string",
        # "internshipName": "string",
        # "about": "string",
        # "requirments": "string"


# class NewInternshipSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Internship
#         fields = (
#         'companyRepresentative', 'program', 'internshipName', 'companyName', 'about', 'requirements', 'mentor')


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

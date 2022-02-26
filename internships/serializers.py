from rest_framework import serializers
from .models import Internship


class InternshipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = ('program', 'internshipName', 'company', 'about', 'requirements')

        # "companyName": "string",
        # "internshipName": "string",
        # "about": "string",
        # "requirments": "string"


class NewInternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = ('companyRepresentative', 'program', 'internshipName', 'company', 'about', 'requirements','mentor')

# "username": "string",
# "companyName": "string",
# "internshipName": "string",
# "about": "string",
# "requirments": "string",
# "mentor": "string"

from rest_framework import serializers

import profile_user
from .models import StudentProfile, CompanyProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('id', 'phone_number', 'birthdate', 'gitLink', 'linkedinLink', 'address', 'picture', 'cv', 'gradesSheet',
                  'student_id')


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ('companyName_id', 'yearEstablish', 'workersAmount', 'location', 'linkedinLink', 'about')


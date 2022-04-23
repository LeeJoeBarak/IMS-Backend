from rest_framework import serializers

import profile_user
from .models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('id', 'phone_number', 'birthdate', 'gitLink', 'linkedinLink', 'address', 'picture', 'cv', 'gradesSheet',
                  'student_id')


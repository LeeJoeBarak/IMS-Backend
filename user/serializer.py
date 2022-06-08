from rest_framework import serializers
# from .models import CompanyRepresentative
#
#

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# User Serializer
from program.models import StudentAndProgram, Program
from user.models import Student, Company, ProgramManager, CompanyRepresentative, CompanyMentor


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class CompanyRepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRepresentative
        fields = ('user_id', 'companyName')


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('companyName',)


class CompanyFullSerializer(serializers.ModelSerializer):
    #     "companyName": "string",
    #     "yearEstablish": 0,
    #     "workersAmount": 0,
    #     "location": "string",
    #     "about": "string"
    class Meta:
        model = Company
        fields = ('companyName', 'yearEstablish', 'workersAmount', 'location', 'about')


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('program',)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('user_id', 'status')


# Register Serializer:

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']

        )
        return user


class StudentProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAndProgram
        fields = ('program_id', 'user_id')


class ProgramManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramManager
        fields = ('user_id',)


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        else:
            raise serializers.ValidationError("Incorrect Credentials")


# UpdatePassword Serializer
class UpdatePasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        else:
            raise serializers.ValidationError("Incorrect Credentials")


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMentor
        fields = ('company_id', 'user_id')

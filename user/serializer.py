# from rest_framework import serializers
# from .models import CompanyRepresentative
#
#

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# User Serializer
from user.models import Student, Company


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('companyName',)


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


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ('user_id', 'status')

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

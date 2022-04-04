from tokenize import String

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from knox.auth import TokenAuthentication
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.models import AuthToken, User
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework.settings import api_settings
from knox.settings import knox_settings
from django.contrib.auth.models import User

from program.models import StudentAndProgram, CompanyMentorAndProgram, CompanyRepresentativeAndProgram, \
    ProgramManagerAndProgram, ProgramCoordinatorAndProgram
from program.serializers import StudentAndProgramSerializers, CompanyMentorAndProgramSerializers, \
    CompanyRepresentativeAndProgramSerializers, ProgramManagerAndProgramSerializers, \
    ProgramCoordinatorAndProgramSerializers
from .models import Student, CompanyMentor, CompanyRepresentative, ProgramManager, ProgramCoordinator, Company, \
    SystemManager
from .serializer import UserSerializer, RegisterSerializer, LoginSerializer, StudentProgramSerializer, \
    ProgramSerializer, UpdatePasswordSerializer, UserDetailsSerializer


# Register API:
# /users/register/student:
class RegisterAPI(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response('A user with the same username already exists', status.HTTP_400_BAD_REQUEST)
        # serializer.is_valid(raise_exception=True)
        user = serializer.save()

        student_user = Student.objects.create(
            user_id=UserSerializer(user, context=self.get_serializer_context()).data['id'])
        student_user.save()
        student_program = StudentAndProgram.objects.create(
            program_id=request.data['program'],
            student_id=UserSerializer(user, context=self.get_serializer_context()).data['id']
        )
        student_program.save()

        return Response(
            content_type='A new user has been added',
            status=status.HTTP_201_CREATED,
        )


# /users/register/companyRep:
class RegisterCompanyRepAPI(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response('A user with the same username already exists', status.HTTP_400_BAD_REQUEST)
        # serializer.is_valid(raise_exception=True)
        user = serializer.save()

        companyRep_user = CompanyRepresentative.objects.create(
            user_id=UserSerializer(user, context=self.get_serializer_context()).data['id'],
            companyName=request.data['companyName'])
        companyRep_user.save()

        company_user = Company.objects.create(
            companyName=companyRep_user.companyName)
        company_user.save()

        return Response(
            content_type='A new user has been added',
            status=status.HTTP_201_CREATED
        )


# /users/register/mentor:
class RegisterMentorAPI(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        companies_list = Company.objects.values_list('companyName', flat=True).order_by('companyName')
        if request.data['companyName'] in companies_list:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response('A user with the same username already exists', status.HTTP_400_BAD_REQUEST)
            user = serializer.save()

            companyMentor_user = CompanyMentor.objects.create(
                user_id=UserSerializer(user, context=self.get_serializer_context()).data['id'],
                company_id=request.data['companyName'])
            companyMentor_user.save()

            return Response(
                content_type='A new user has been added',
                status=status.HTTP_201_CREATED
            )
        else:
            return Response('This company does not exist', status.HTTP_404_NOT_FOUND)


# /users/register/programCoordinator:
class RegisterProgramCoordinatorAPI(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response('A user with the same username already exists', status.HTTP_400_BAD_REQUEST)
        # serializer.is_valid(raise_exception=True)
        user = serializer.save()

        programCoordinator_user = ProgramCoordinator.objects.create(
            user_id=UserSerializer(user, context=self.get_serializer_context()).data['id'])
        programCoordinator_user.save()
        return Response(
            content_type='A new user has been added',
            status=status.HTTP_201_CREATED
        )


# /users/register/programManager
class RegisterProgramManagerAPI(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response('A user with the same username already exists', status.HTTP_400_BAD_REQUEST)
        # serializer.is_valid(raise_exception=True)
        user = serializer.save()

        programManager_user = ProgramManager.objects.create(
            user_id=UserSerializer(user, context=self.get_serializer_context()).data['id'])
        programManager_user.save()
        return Response(
            content_type='A new user has been added',
            status=status.HTTP_201_CREATED
        )


# /users/register/systemManager
# Login API
class LoginAPI(generics.GenericAPIView):
    # authentication_classes = ()
    permission_classes = ()
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    # permission_classes = (IsAuthenticated,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response('Invalid username/password supplied', status.HTTP_401_UNAUTHORIZED)
        user = serializer.validated_data
        # _, token = AuthToken.objects.create(user, knox_settings.TOKEN_TTL)
        token = AuthToken.objects.create(user, knox_settings.TOKEN_TTL)[1]
        newToken = token[0:8]
        # Check the model of the user:
        # student
        model = Student.objects.filter(user_id=user.id).first()
        if model is not None:
            program = StudentAndProgram.objects.filter(student_id=user.id).first()
            if program is not None:
                dataProgram = StudentAndProgramSerializers(program)
        if model is None:
            model = CompanyMentor.objects.filter(user_id=user.id).first()
            if model is not None:
                program = CompanyMentorAndProgram.objects.filter(companyMentor_id=user.id).first()
                if program is not None:
                    dataProgram = CompanyMentorAndProgramSerializers(program)
            if model is None:
                model = CompanyRepresentative.objects.filter(user_id=user.id).first()
                if model is not None:
                    program = CompanyRepresentativeAndProgram.objects.filter(companyRepresentative_id=user.id).first()
                    if program is not None:
                        dataProgram = CompanyRepresentativeAndProgramSerializers(program)
                if model is None:
                    model = ProgramManager.objects.filter(user_id=user.id).first()
                    if model is not None:
                        program = ProgramManagerAndProgram.objects.filter(programManager_id=user.id).first()
                        if program is not None:
                            dataProgram = ProgramManagerAndProgramSerializers(program)
                    if model is None:
                        model = ProgramCoordinator.objects.filter(user_id=user.id).first()
                        if model is not None:
                            program = ProgramCoordinatorAndProgram.objects.filter(programCoordinator_id=user.id).first()
                            if program is not None:
                                dataProgram = ProgramCoordinatorAndProgramSerializers(program)

                        if model is None:
                            model = SystemManager.objects.filter(user_id=user.id).first()
                            if model is not None:
                                data = UserSerializer(user, context=self.get_serializer_context()).data
                                return Response({
                                    "userType": model.__str__(),
                                    "username": data['username'],
                                    "firstName": data['first_name'],
                                    "session": newToken,
                                })
        # print(token)

        # print("newToken: ", newToken)
        if model is not None:
            user_logged_in.send(sender=user.__class__, request=request, user=user)
            if program is None:
                program_id = ''
            else:
                program_id = dataProgram.data['program_id']
            data = UserSerializer(user, context=self.get_serializer_context()).data
            return Response({
                "userType": model.__str__(),
                "username": data['username'],
                "firstName": data['first_name'],
                "session": newToken,
                "program": program_id
            })

        # Student.objects.filter(student_id=user.id).first()
        return Response('Invalid username/password supplied', status.HTTP_401_BAD_REQUEST)


# Logout API
class LogoutAPI(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    permission_classes = ()

    def post(self, request, format=None):
        # auth_token.delete()
        # print("request.data['Authorization']: ", request.data['Authorization'])
        obj = AuthToken.objects.get(token_key=request.data['Authorization'])
        # print("AuthToken.objects.get(token_key=): ", obj)
        obj.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response('successful logout', status=status.HTTP_204_NO_CONTENT)


# /users/changePsw:
class UpdatePassword(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UpdatePasswordSerializer

    def post(self, request):
        # print("request.data: ", request.data)
        if request.data['new_password'] == request.data['old_password']:
            return Response('Invalid username/password supplied', status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=request.data['username'], password=request.data['old_password'])
        # print("user: ", user)
        if user is not None:
            user.set_password(request.data['new_password'])
            user.save()
        else:
            return Response('Invalid username/password supplied', status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            content_type='successful change the password',
            status=status.HTTP_201_CREATED,
        )

from django.shortcuts import get_object_or_404
from knox.auth import TokenAuthentication
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework.settings import api_settings

from .models import Student, CompanyMentor, CompanyRepresentative, ProgramManager, ProgramCoordinator
from .serializer import UserSerializer, RegisterSerializer, LoginSerializer


# Register API
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
        return Response(
            content_type='A new user has been added',
            status=status.HTTP_201_CREATED,
            data={
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


# Login API
class LoginAPI(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    # authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    # permission_classes = (IsAuthenticated,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response('Invalid username/password supplied', status.HTTP_401_UNAUTHORIZED)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        # Check the model of the user:
        model = Student.objects.filter(user_id=user.id).first()
        if model is None:
            model = CompanyMentor.objects.filter(user_id=user.id).first()
            if model is None:
                model = CompanyRepresentative.objects.filter(user_id=user.id).first()
                if model is None:
                    model = ProgramManager.objects.filter(user_id=user.id).first()
                    if model is None:
                        model = ProgramCoordinator.objects.filter(user_id=user.id).first()

        if model is not None:
            # user_logged_in.send(sender=request.user.__class__,
            #                     request=request, user=request.user)

            return Response({
                "type": model.__str__(),
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": token
            })

        # Student.objects.filter(student_id=user.id).first()
        return Response('Invalid username/password supplied', status.HTTP_401_BAD_REQUEST)


# Logout API
class LogoutAPI(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request._auth.delete()
        # user_logged_out.send(sender=request.user.__class__,
        #                      request=request, user=request.user)
        return Response('successful logout', status=status.HTTP_204_NO_CONTENT)

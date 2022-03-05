from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import status

from .models import Student
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
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })

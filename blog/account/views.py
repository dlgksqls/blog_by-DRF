from django.shortcuts import render
from rest_framework import serializers
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserModelSerializers, SignUpSerializers
from .models import User

# Create your views here.


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializers


@api_view(["POST"])
def UserSignUpView(request):
    serializer = SignUpSerializers(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        User = serializer.save()
        User.set_password(password)
        User.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserSignupView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = SignUpSerializers

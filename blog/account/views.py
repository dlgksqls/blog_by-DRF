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
    serlizer = SignUpSerializers(data=request.data)

    if serlizer.is_valid():
        username = serlizer.validated_data.get("username")
        email = serlizer.validated_data.get("email")
        password = serlizer.validated_data.get("password")

        User = serlizer.save()
        User.set_password(password)
        User.save()

        return Response(serlizer.data, status=status.HTTP_201_CREATED)

    return Response(serlizer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserSignupView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = SignUpSerializers

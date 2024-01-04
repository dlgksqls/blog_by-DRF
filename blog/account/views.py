from django.shortcuts import render
from django.shortcuts import get_object_or_404
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


# @api_view(["GET"])
# def UserDetailView(request, username):
#     user = get_object_or_404(User, username=username)
#     serializer = UserModelSerializers(user)
#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["GET", "PATCH"])
# def UserModifyView(request, username):
#     user = get_object_or_404(User, username=username)
#     if request.method == "GET":
#         serializer = UserModelSerializers(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "PATCH":
#         serializer = UserModelSerializers(user, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(
#             {"detail": "Invalid request method"},
#             status=status.HTTP_405_METHOD_NOT_ALLOWED,
#         )


@api_view(["GET", "PATCH", "DELETE"])
def UserDetailView(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == "GET":  # 유저 정보
        serializer = UserModelSerializers(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PATCH":  # 유저 수정
        serializer = UserModelSerializers(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":  # 유저 삭제
        user.delete()
        return Response({"detail": "Delete Complete"}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(
            {"detail": "Invalid request method"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.authentication import authenticate
from django.http import Http404
import jwt
from blog.settings import SECRET_KEY

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

        # jwt 접근
        token = TokenObtainPairSerializer.get_token(User)
        refresh_token = str(token)
        access_token = str(token.access_token)
        res = Response(
            {
                "user": serializer.data,
                "message": "register.success",
                "token":{
                    "access": access_token,
                    "refresh": refresh_token
                },
            },
            status=status.HTTP_200_OK,
        )

        # jwt 토근 => 쿠키에 저장
        res.set_cookie("access", access_token, httponly=True)
        res.set_cookie("refresh", refresh_token, httponly=True)

        return res
        #return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def UserLogInView(request):
    user = authenticate(
        username = request.data.get("username"),
        password = request.data.get("password")
    )
    
    if user is not None:
        serializer = UserModelSerializers(user)
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        res = Response(
            {
                "user": serializer.data,
                "message": "login success",
                "token":{
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
            status=status.HTTP_200_OK,
        )
        res.set_cookie("access", access_token, httponly=True)
        res.set_cookie("refresh", refresh_token, httponly=True)
        return res
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



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
def UserDetailView(request): 
    # user = get_object_or_404(User, username=username)
    # if request.method == "GET":  # 유저 정보
    #     serializer = UserModelSerializers(user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "GET":
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserModelSerializers(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserModelSerializers(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)

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

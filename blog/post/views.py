from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
import jwt

from rest_framework.authentication import TokenAuthentication

from core.permission import IsOwnerOnly
from .models import Post, Comment
from .serializers import PostModelSerializers, CommentModelSerializers
from account.serializers import UserModelSerializers
from account.models import User
from blog.settings import SECRET_KEY

# Create your views here.


class PostListView(generics.ListAPIView):
    permission_classes = [IsOwnerOnly]
    serializer_class = PostModelSerializers

    def get_queryset(self):
        # 요청한 사용자의 정보를 가져옴
        writer = self.request.user
        # 요청한 사용자가 작성한 게시물만 필터링
        return Post.objects.filter(writer=writer)


@api_view(["GET", "PATCH", "DELETE"])
def PostDetailView(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "GET":
        # IsOwnerOnly 인스턴스 생성
        permission = IsOwnerOnly()
        # 요청에 대한 s권한 확인
        if not permission.has_object_permission(request, None, post):
            return HttpResponseForbidden()
        else:
            serializer = PostModelSerializers(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = PostModelSerializers(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        post.delete()
        return Response({"detail": "Delete Complete"}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(
            {"detail": "Invalid request method"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

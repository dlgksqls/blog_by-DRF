from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.authentication import TokenAuthentication

from core.permission import IsOwnerOnly
from .models import Post, Comment
from .serializers import PostModelSerializers, CommentModelSerializers
from blog.settings import SECRET_KEY

# Create your views here.


class PostListView(generics.ListAPIView):
    permission_classes = [IsOwnerOnly]
    serializer_class = PostModelSerializers

    def get_queryset(self):
        writer = self.request.user
        return Post.objects.filter(writer=writer)


@api_view(["GET", "PATCH", "DELETE"])
def PostDetailView(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "GET":
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

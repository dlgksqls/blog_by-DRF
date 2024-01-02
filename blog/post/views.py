from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostModelSerializers, CommentModelSerializers

# Create your views here.

class PostListView(generics.ListAPIView):
  queryset = Post.objects.all()
  serializer_class = PostModelSerializers

@api_view(["GET"])
def PostDetailView(request, id):
  post = get_object_or_404(Post, id = id)
  serializer = PostModelSerializers(post)
  return Response(serializer.data, status=status.HTTP_200_OK)
  
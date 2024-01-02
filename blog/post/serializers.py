from rest_framework.serializers import ModelSerializer
from .models import Post, Comment

class PostModelSerializers(ModelSerializer):
  class Meta:
    model = Post
    fields = '__all__'

class CommentModelSerializers(ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'
from django.contrib import admin
from account.models import User
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ("id", "image", "content", "created_at", "writer")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ("username", "email")
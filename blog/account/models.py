from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager

# Create your models here.


class UserManager(DjangoUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("이메일을 입력해줴요.")

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()

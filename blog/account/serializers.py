from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
    ValidationError,
)
from rest_framework.validators import UniqueValidator

from django.contrib.auth.password_validation import validate_password
from .models import User


class UserModelSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SignUpSerializers(ModelSerializer):
    username = CharField(max_length=150)
    email = EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "password", "password2", "email"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user

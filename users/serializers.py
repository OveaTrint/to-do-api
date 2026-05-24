from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = CustomUser
        fields = ["username", "email", "password"]

    def validate_password(self, unhashed_pw):
        validate_password(unhashed_pw)
        return unhashed_pw

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data["username"], email=validated_data["email"]
        )
        # Hashes password before saving
        user.set_password(validated_data["password"])
        user.save()

        return user

from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


def get_access_and_refresh_token(user: AbstractBaseUser):
    """Get the access and refresh JWT tokens for the current user"""
    if not user.is_active:
        raise AuthenticationFailed("User is not active")

    tokens = RefreshToken.for_user(user)
    return {
        "access": str(tokens.access_token),
        "refresh": str(tokens),
    }

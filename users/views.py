from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import UserSerializer
from users.services import get_access_and_refresh_token

# Create your views here.


@extend_schema(request=UserSerializer)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response(
            get_access_and_refresh_token(user), status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            data={"detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(request=UserSerializer)  # for swagger docs
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    supplied_email = request.data["email"]
    supplied_password = request.data["password"]

    try:
        user = CustomUser.objects.get(email=supplied_email)
        if user.check_password(supplied_password):
            return Response(
                get_access_and_refresh_token(user), status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Invalid password, please try again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except CustomUser.DoesNotExist:
        return Response(
            {"detail": "User not found, please register first."},
            status.HTTP_404_NOT_FOUND,
        )

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import Response

from users.models import CustomUser
from users.serializers import UserRegisterSerializer
from utils.jwt import get_jwt

# Create your views here.


@api_view(["POST"])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        # generate jwt token with user email as payload
        jwt_payload = {"email": serializer.validated_data["email"]}
        jwt = get_jwt(jwt_payload)

        return Response({"token": jwt}, status=status.HTTP_201_CREATED)

    return Response(
        data={"status": "error", "detail": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
def login_user(request):
    supplied_email = request.data["email"]
    supplied_password = request.data["password"]

    try:
        user = CustomUser.objects.get(email=supplied_email)
        if user.check_password(supplied_password):
            jwt_payload = {"email": supplied_email}
            return Response({"token": get_jwt(jwt_payload)}, status.HTTP_200_OK)

        else:
            return Response(
                {"status": "error", "detail": "Invalid password, please try again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except CustomUser.DoesNotExist:
        return Response(
            {"status": "error", "detail": "User not found, please register first."},
            status.HTTP_404_NOT_FOUND,
        )

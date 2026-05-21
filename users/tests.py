from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from utils.jwt import get_jwt

# Create your tests here.


class UserAPITestCase(APITestCase):
    register_url = reverse("users:register")
    login_url = reverse("users:login")

    def setUp(self) -> None:
        data = {
            "username": "Kamal",
            "email": "kbaiyewu@gmail.com",
            "password": "Ilovemymom101",
        }

        self.client.post(
            UserAPITestCase.register_url,
            data,
        )

    def test_create_account(self):
        """
        Ensure we can create an account
        """
        # Data passed for registration
        data = {
            "username": "Kamal201",
            "email": "kbaiyewu109@gmail.com",
            "password": "Ilovemymom101",
        }

        response = self.client.post(UserAPITestCase.register_url, data)

        # payload for jwt token w/o username and password
        data.pop("password")
        data.pop("username")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"token": get_jwt(data)})

    def test_unique_email_constraint(self):
        """
        Test whether unique email constraint holds
        """
        data = {
            "username": "Kamal101",
            "email": "kbaiyewu@gmail.com",
            "password": "Ilovemymom101",
        }

        response = self.client.post(UserAPITestCase.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "status": "error",
                "detail": {"email": ["user with this email already exists."]},
            },
        )

    def test_valid_login(self):
        data = {"email": "kbaiyewu@gmail.com", "password": "Ilovemymom101"}
        response = self.client.post(UserAPITestCase.login_url, data=data)

        data.pop("password")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"token": get_jwt(data)})

    def test_login_with_invalid_email(self):
        data = {"email": "kbiyewu@gmail.com", "password": "Ilovemymom101"}
        response = self.client.post(UserAPITestCase.login_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(),
            {"status": "error", "detail": "User not found, please register first."},
        )

    def test_login_with_invalid_password(self):
        data = {"email": "kbaiyewu@gmail.com", "password": "ilovemymom10"}
        response = self.client.post(UserAPITestCase.login_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {"status": "error", "detail": "Invalid password, please try again."},
        )

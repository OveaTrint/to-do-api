from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser

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
        Ensures we can create an account
        """
        # Data passed for registration
        data = {
            "username": "Kamal201",
            "email": "kbaiyewu109@gmail.com",
            "password": "Ilovemymom101",
        }

        response = self.client.post(UserAPITestCase.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertIsNotNone(CustomUser.objects.get(email=data["email"]))

    def test_unique_email_constraint(self):
        """
        Tests whether the unique email constraint holds
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
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(username=data["username"])

    def test_valid_login(self):
        """
        Test whether API authenticates user when valid login credentials are provided
        """
        data = {"email": "kbaiyewu@gmail.com", "password": "Ilovemymom101"}
        response = self.client.post(UserAPITestCase.login_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # checks if response contains access and refresh tokens
        self.assertTrue("access" in response.json())
        self.assertTrue("refresh" in response.json())

    def test_login_with_invalid_email(self):
        """
        Test whether API returns an error user when valid login credentials are provided
        """
        data = {"email": "kbiyewu@gmail.com", "password": "Ilovemymom101"}
        response = self.client.post(UserAPITestCase.login_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(),
            {"status": "error", "detail": "User not found, please register first."},
        )

        # checks if access and refresh tokens are not in the response
        self.assertTrue("access" not in response.json())
        self.assertTrue("access" not in response.json())

    def test_login_with_invalid_password(self):
        """
        Test whether server authenticates user when valid login credentials are provided
        """
        data = {"email": "kbaiyewu@gmail.com", "password": "ilovemymom10"}
        response = self.client.post(UserAPITestCase.login_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {"status": "error", "detail": "Invalid password, please try again."},
        )
        self.assertTrue("access" not in response.json())
        self.assertTrue("refresh" not in response.json())

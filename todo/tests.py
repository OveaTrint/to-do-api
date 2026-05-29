from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser

from .models import ToDo

# Create your tests here.


class ToDoItemTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = CustomUser.objects.create_user(
            "kamal", "kbaiyewu@gmail.com", "ilovepeople"
        )

    def test_create_todo(self):
        ToDo.objects.create(
            title="Food",
            description="Buy groceries from bokku",
            owner=self.user1,
        )

        self.assertEqual(ToDo.objects.count(), 1)

    def test_create_todo_no_owner(self):
        with self.assertRaises(IntegrityError):
            ToDo.objects.create(
                title="Food",
                description="Buy groceries from bokku",
            )

    def test_blank_title(self):
        with self.assertRaises(IntegrityError):
            ToDo.objects.create(title="", description="Nothing", owner=self.user1)

    def test_blank_description(self):
        with self.assertRaises(IntegrityError):
            ToDo.objects.create(title="Nothing", description="", owner=self.user1)


class ToDoItemAPITestCaseNoAuth(APITestCase):
    """Test creating an item with no auth"""

    def test_create_item_no_authorization(self):
        url = reverse("todo")
        data = {"title": "shopping", "description": "Buy bread from bokku "}
        response = self.client.post(url, data)

        error_response = {"detail": "Authentication credentials were not provided."}
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), error_response)


class ToDoItemAPITestCaseAuth(APITestCase):
    url = reverse("todo")

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            "user1", "user1@gmail.com", "user12099@"
        )
        tokens = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens.access_token}")

    def test_create_todo(self):
        data = {"title": "shopping", "description": "Buy bread from bokku "}
        response = self.client.post(ToDoItemAPITestCaseAuth.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertContains(response, "id", status_code=status.HTTP_201_CREATED)
        self.assertContains(response, "title", status_code=status.HTTP_201_CREATED)
        self.assertContains(
            response, "description", status_code=status.HTTP_201_CREATED
        )

    def test_update_todo(self):
        ToDo.objects.create(
            title="Religion", description="Go to the mosque", owner=self.user
        )
        id = ToDo.objects.get(title="Religion").pk

        url = reverse(ToDoItemAPITestCaseAuth.url, args=[id])

        data = {"title": "Eat", "description": "Eat breakfast"}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "id")
        self.assertContains(response, "title")
        self.assertContains(response, "description")

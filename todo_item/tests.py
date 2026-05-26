import logging

from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from todo_item.serializer import ToDoItemSerializer
from users.models import CustomUser

from .models import ToDoItem

# Create your tests here.


def get_user(pk: int):
    user = CustomUser.objects.get(pk=pk)

    return user


class ToDoItemTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = CustomUser.objects.create_user(
            "kamal", "kbaiyewu@gmail.com", "ilovepeople"
        )

    def test_create_todo_item(self):
        ToDoItem.objects.create(
            title="Food",
            description="Buy groceries from bokku",
            owner=self.user1,
        )

        self.assertTrue(ToDoItem.objects.count(), 1)

    def test_create_todo_item_no_owner(self):
        with self.assertRaises(IntegrityError):
            ToDoItem.objects.create(
                title="Food",
                description="Buy groceries from bokku",
            )

    def test_blank_title(self):
        with self.assertRaises(IntegrityError):
            ToDoItem.objects.create(title="", description="Nothing", owner=self.user1)

    def test_blank_description(self):
        with self.assertRaises(IntegrityError):
            ToDoItem.objects.create(title="Nothing", description="", owner=self.user1)


class CreateToDoItemAPITestCaseNoAuth(APITestCase):
    """Test creating an item with no auth"""

    def test_create_item_no_authorization(self):
        url = reverse("todo_item:create_todo")
        data = {"title": "shopping", "description": "Buy bread from bokku "}
        response = self.client.post(url, data)

        error_response = {"detail": "Authentication credentials were not provided."}
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), error_response)


class CreateToDoItemAPITestCaseAuth(APITestCase):
    url = reverse("todo_item:create_todo")

    def setUp(self):
        user = CustomUser.objects.create_user("user1", "user1@gmail.com", "user12099@")
        tokens = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens.access_token}")

    def test_create_item_with_auth(self):
        data = {"title": "shopping", "description": "Buy bread from bokku "}

        response = self.client.post(CreateToDoItemAPITestCaseAuth.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response.json(), ToDoItemSerializer(data=data))

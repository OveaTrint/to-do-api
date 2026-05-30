from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser

from .models import ToDo


# Create your tests here.
class ToDoURL:
    base_url = reverse_lazy("todo:todo-list")

    def param_url(self, id: int):
        return reverse_lazy("todo:todo-detail", args=[id])


urls = ToDoURL()


class ToDoTestCase(TestCase):
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


class ToDoAPITestCaseNoAuth(APITestCase):
    """Test creating an item with no auth"""

    def test_create_item_no_authorization(self):
        data = {"title": "shopping", "description": "Buy bread from bokku "}
        response = self.client.post(urls.base_url, data)

        error_response = {"detail": "Authentication credentials were not provided."}
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), error_response)


class ToDoAPITestCaseAuth(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            "user1", "user1@gmail.com", "user12099@"
        )
        tokens = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens.access_token}")

    def test_create_todo(self):
        data = {"title": "shopping", "description": "Buy bread from bokku "}
        response = self.client.post(urls.base_url, data)

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

        data = {"title": "Eat", "description": "Eat breakfast"}
        response = self.client.put(urls.param_url(id), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "id")
        self.assertContains(response, "title")
        self.assertContains(response, "description")

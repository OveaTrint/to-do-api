from django.db.utils import IntegrityError
from django.test import TestCase

from users.models import CustomUser

from .models import ToDoItem

# Create your tests here.


def get_user(pk: int):
    user = CustomUser.objects.get(pk=pk)

    return user


class ToDoItemTestCase(TestCase):
    def setUp(self) -> None:
        CustomUser.objects.create_user("kamal", "kbaiyewu@gmail.com", "ilovepeople")
        CustomUser.objects.create_user("usman", "usman2099@gmail.com", "ilovefamily")
        CustomUser.objects.create_user("Nini", "ninilola2010@gmail.com", "iloveAllaha")

    def test_create_todo_item(self):
        ToDoItem.objects.create(
            title="Food",
            description="Buy groceries from bokku",
            owner=get_user(1),
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
            ToDoItem.objects.create(title="", description="Nothing", owner=get_user(2))

    def test_blank_description(self):
        with self.assertRaises(IntegrityError):
            ToDoItem.objects.create(title="Nothing", description="", owner=get_user(2))

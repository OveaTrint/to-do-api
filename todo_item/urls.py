from django.urls import path

from todo_item.views import create_todo

app_name = "todo_item"

urlpatterns = [
    path("todos/", create_todo, name="create_todo"),
]

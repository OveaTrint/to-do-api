from rest_framework import serializers

from .models import ToDoItem


class ToDoItemSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = ToDoItem
        fields = ["title", "description"]

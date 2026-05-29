from rest_framework import serializers

from .models import ToDo


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = ToDo
        fields = ["id", "title", "description"]

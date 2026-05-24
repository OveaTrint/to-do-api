from django.db import models

from users.models import CustomUser


# Create your models here.
class ToDoItem(models.Model):
    title = models.CharField()
    description = models.CharField(max_length=100)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

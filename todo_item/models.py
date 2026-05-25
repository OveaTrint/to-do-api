from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.constraints import CheckConstraint
from django.db.models.functions import Length

from users.models import CustomUser

models.CharField.register_lookup(Length)


def check_empty_title_or_description(value):
    if len(value) == 0:
        raise ValidationError("Title or description fields must not be empty")


# Create your models here.
class ToDoItem(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            CheckConstraint(
                condition=Q(title__length__gte=1) & Q(description__length__gte=1),
                name="title_and_description_not_empty",
            )
        ]

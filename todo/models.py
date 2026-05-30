from django.db import models
from django.db.models import Q
from django.db.models.constraints import CheckConstraint
from django.db.models.functions import Length

from users.models import CustomUser

models.CharField.register_lookup(Length)


# Create your models here.
class ToDo(models.Model):
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

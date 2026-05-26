from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # makes email be used as the identifier for auth
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser) :
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=200, unique = True)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = []
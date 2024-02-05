from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Token(models.Model):
    user_name = models.CharField(max_length=45)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
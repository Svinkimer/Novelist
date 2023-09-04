from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    telegram = models.CharField(max_length=32, blank=True, null=True)

# Create your models here.

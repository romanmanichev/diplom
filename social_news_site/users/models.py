from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    photo = models.ImageField(upload_to="photos/users/", blank=True, null=True)
    message_count = models.IntegerField(default=0)


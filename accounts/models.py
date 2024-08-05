from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    purpose = models.TextField()

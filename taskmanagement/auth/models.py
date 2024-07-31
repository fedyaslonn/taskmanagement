from django.contrib.auth.models import AbstractUser
from django.db import models
from .celerytask import send_email
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=False)
    username = models.CharField(max_length=30, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

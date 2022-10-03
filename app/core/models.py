from email.policy import default
from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique = True)
    name = models.CharField(max_length = 20)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

def __str__(self):
    return self.email
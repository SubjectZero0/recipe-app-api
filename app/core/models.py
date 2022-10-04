from enum import unique
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

class CustomUserManager(BaseUserManager):
    """Custom manager for the custom user model"""

    def create_user(self, email, name, password=None):
        """Method to create a regular user"""

        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(
            email = self.normalize_email(email),
            name = name,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, name, password):
        """Method to create a superuser"""

        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    """Custom User model"""

    email = models.EmailField(unique = True)
    name = models.CharField(max_length = 20)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
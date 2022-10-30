from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

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

############################################################

def image_path(instance, filename):
    """Function to explicitly create a path in MEDIA_ROOT for recipe images"""
    return 'images/{filename}'.format(filename=filename)


class Recipe(models.Model):
    """
    Recipes Model
    Recipes are created by authenticated users
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'recipes')
    recipe_title = models.CharField(max_length = 100)
    recipe_description = models.TextField()
    recipe_instructions = models.TextField()
    tags = models.ManyToManyField('core.Tag', blank = True)
    ingredients = models.ManyToManyField('core.Ingredient', blank = True)
    image = models.ImageField(upload_to = image_path, height_field = None, width_field = None, max_length=200, blank = True, null = True)

    def __str__(self):
        return self.recipe_title

#############################################################

class Tag(models.Model):
    """
    Tag model for adding to recipes.
    Intended for authenticated users.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'tags')
    tag_name = models.CharField(max_length = 100)

    def __str__(self):
        return self.tag_name


#############################################################

class Ingredient(models.Model):
    """
    Ingredient model for adding to recipes
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'ingredients')
    ingredient_name = models.CharField(max_length = 100)

    def __str__(self):
        return self.ingredient_name

#############################################################


from django.contrib import admin
from .models import CustomUserModel, Recipe
# Register your models here.

admin.site.register(CustomUserModel)
admin.site.register(Recipe)
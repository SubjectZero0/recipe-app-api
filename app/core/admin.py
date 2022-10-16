from django.contrib import admin
from .models import CustomUserModel, Recipe, Tag
# Register your models here.

admin.site.register(CustomUserModel)
admin.site.register(Recipe)
admin.site.register(Tag)
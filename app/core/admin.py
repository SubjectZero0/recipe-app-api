from django.contrib import admin
from .models import CustomUserModel, Recipe, Tag, Ingredient

# Register your models here.

admin.site.register(CustomUserModel)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
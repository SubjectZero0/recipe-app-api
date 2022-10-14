
from urllib import request
from rest_framework.serializers import ModelSerializer
from core.models import Recipe
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.fields import CurrentUserDefault

class RecipeSerializer(ModelSerializer):
    """Serializer for Recipe API"""

    class Meta:
        model = Recipe
        fields = '__all__'
        extra_kwargs = {'user':{'read_only':True}}







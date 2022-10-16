from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,Serializer
from core.models import Recipe, Tag
from django.contrib.auth import get_user_model


class RecipeTagSerializer(ModelSerializer):
    """
    Serializer for user's recipe tags
    Only want to show tag_name
    """
    class Meta:
        model = Tag
        fields = [ 'id', 'tag_name']
        read_only_fields =['id']

class RecipeSerializer(ModelSerializer):
    """Serializer for Recipe API"""

    tags = RecipeTagSerializer(many=True, required = False)

    class Meta:
        model = Recipe
        fields = '__all__'
        extra_kwargs = {
            'user':{'read_only':True},
            'id':{'read_only':True}
        }

    def _get_or_create_tags(self, tags, recipe):
        """
        Get or create tags, if non exist.
        ADDS the new tags in the recipe.
        """
        authenticated_user = self.context['request'].user #gets the authenticated user that makes the post request.

        for tag in tags:
            """
            for every tag, if it exists in the Tag objects already, get it and add it to the recipe as a relationship.
            If it doesnt exist, create a Tag object (available in the Tag API) and add it to the recipe as a relationship.
            """
            tag_obj, created = Tag.objects.get_or_create(user=authenticated_user, **tag) #in case of creation, tag object will be created with 'user'=authenticated_user.

            recipe.tags.add(tag_obj) #adds the tag object in the recipe, instead of a direct post request, which is not allowed.


    def create(self, validated_data):
        """
        Custom Method for Creating a recipe, with
        nested serializer - RecipeTagSerializer,
        since direct creation with nested serializers is not allowed.
        If a Tag doesnt exist in the Tag table, it will be created,
        and will be available in the Tag API.
        """

        tags = validated_data.pop('tags', []) #if any tags are passed into the serializer, removes them and places them in tags variable. Else its an empty list.
        recipe = Recipe.objects.create(**validated_data) #creates a recipe with the rest of the validated data.
        self._get_or_create_tags(tags, recipe)

        return recipe

    def update(self, instance, validated_data):
        """
        As with creation, custom method for updating recipe
        """
        tags = validated_data.pop('tags', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
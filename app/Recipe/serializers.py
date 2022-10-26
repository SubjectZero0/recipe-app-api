from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from core.models import Recipe, Tag, Ingredient




class RecipeTagSerializer(ModelSerializer):
    """
    Serializer for user's recipes tags.
    Tags can be created through creating a recipe with tags,
    or by the Tag API.

    """
    class Meta:
        model = Tag
        fields = [ 'id', 'tag_name']
        read_only_fields =['id']


class RecipeIngredientSerializer(ModelSerializer):
    """
    Serializer for user's recipes' ingredients.
    Ingredients can be created through creating recipes
    with ingredients, or through the Ingredient API.
    """

    class Meta:
        model = Ingredient
        fields = ['id', 'ingredient_name']
        read_only_fields = ['id']


class RecipeImageSerializer(ModelSerializer):
    """
    Serializer for recipe image(s).
    Images can only be uploaded by authenticated users.
    Image upload requires recipe id (recipe detail).
    """
    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {
            'image':{'required' : True}
            }

###########################################################################################


class RecipeSerializer(ModelSerializer):
    """
    Serializer for Recipes.
    Automatic Tag and Ingredient creation and update in Tag/Ingredient API,
    through many-to-many relationship.
    """

    tags = RecipeTagSerializer(many=True, required = False) #use of nested serializer
    ingredients = RecipeIngredientSerializer(many=True, required=False) #use of nested serializer
    image = serializers.ImageField(required = False, read_only = True)
    class Meta:
        model = Recipe
        fields = '__all__'
        extra_kwargs = {
            'user':{'read_only':True},
            'id':{'read_only':True}
        }

    def _get_or_create_tags(self, tags, recipe):
        """
        Helper Function.
        Get, or create tags, if non exist.
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

    def _get_or_create_ingredients(self, ingredients, recipe):
        """
        Helper function.
        Get, or create ingredients, if non exist.
        ADDS the new ingredients in the recipe.
        """
        authenticated_user = self.context['request'].user

        for ingredient in ingredients:
            ingr_obj, created = Ingredient.objects.get_or_create(user=authenticated_user, **ingredient)
            recipe.ingredients.add(ingr_obj)


    def create(self, validated_data):
        """
        Custom Method for Creating a recipe, with
        nested serializers, since direct creation
        with nested serializers/manytomany is not allowed.
        If a Tag/Ingredient doesnt exist in the appropriate table,
        it will be created, and will be available in the Tag/Ingredient API.
        """

        tags = validated_data.pop('tags', []) #if any tags are passed into the serializer, removes them and places them in tags variable. Else its an empty list.
        ingredients = validated_data.pop('ingredients', []) #if any ingredients are passed into the serializer, removes them and places them in tags variable. Else its an empty list.
        recipe = Recipe.objects.create(**validated_data) #creates a recipe with the rest of the validated data.
        self._get_or_create_tags(tags, recipe)#calls helper function to get or create tags and ADD them to recipe.
        self._get_or_create_ingredients(ingredients, recipe) #calls helper function to get or create ingredients and ADD them to recipe.

        return recipe

    def update(self, instance, validated_data):
        """
        As with creation, custom method for updating recipe
        """
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)

        if tags is not None:
            """
            if tags exist, clears them.
            Calls helper function to create tags and ADD them to instance(recipe)
            """
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        if ingredients is not None:
            """
            if ingredients exist, clears them.
            Calls helper function to create ingredients and ADD them to instance(recipe)
            """
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            """
            Sets the attributes of the instance to the new values.
            This is the updating part.
            """
            setattr(instance, attr, value)

        instance.save()

        return instance
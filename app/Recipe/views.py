
from core.models import Ingredient, Recipe, Tag
from .serializers import RecipeSerializer, RecipeTagSerializer, RecipeIngredientSerializer, RecipeImageSerializer
from .permissions import UpdateMyRecipesPermissions

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class BaseRecipeViewSet(ModelViewSet):
    """
    Base Viewset for Recipe and My_Recipe API.
    """
    queryset = Recipe.objects.all()#Users can GET all recipes
    authentication_classes = [TokenAuthentication]
    filter_backends = [SearchFilter]

    search_fields = [
        'recipe_title',
        'recipe_description',
        ]

    def perform_create(self, serializer):
        """
        Creates a recipe instance with 'user'= the user that makes the request.
        Automatically GETS the token authenticated user.
        """
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        """
        Updates a recipe instance with 'user'= the user that makes the request.
        Automatically GETS the token authenticated user.
        """
        instance = serializer.save(user=self.request.user)
        return instance

    def get_serializer_class(self):
        """
        Method to get the correct serializer, depending
        if the user wants to create/update a recipe,
        or upload an image.
        """
        if self.action == 'upload_recipe_image':
            serializer = RecipeImageSerializer
        else:
            serializer = RecipeSerializer
        return serializer

    @action(methods = ['POST'], detail = True, url_path = 'upload-image', url_name='img_upload')
    def upload_recipe_image(self, request, pk=None):
        """
        Custom 'POST' endpoint with custom url, for uploading a recipe image.
        This action requires recipe id and a token authenticated user.
        The only way to upload an image is through this action.

        """
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeApiViewset(BaseRecipeViewSet):
    """
    Handles All-Recipe API requests.
    User has to be authenticated to create update and delete, but not to retrieve.
    User can only update and delete the recipes they have created.
    Image field is read only. Go to '/api/recipes/{id}/image-upload,
    to upload a recipe image.
    """
    #User has to be authenticated to create. They can only update their own recipes
    permission_classes = [IsAuthenticatedOrReadOnly, UpdateMyRecipesPermissions]

class MyRecipesApiViewset(BaseRecipeViewSet):
    """
    Handles My_Recipe API requests.
    User has to be authenticated and can only retrieve their own recipes.
    User has to be authenticated to create, update and delete.
    User can only update and delete the recipes they have created.
    Image field is read only. Go to '/api/my_recipes/{id}/image-upload,
    to upload a recipe image.

    """
    permission_classes = [IsAuthenticated,UpdateMyRecipesPermissions]

    def get_queryset(self):
        """
        The queryset is modified to only look for the recipes
        the user has created
        """
        query = Recipe.objects.filter(user=self.request.user)
        return query

##################################################################################

class BaseRecipeAttrsViewSet(ModelViewSet):
    """
    Base viewset for Tag and Ingredient APIs.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        """
        Creates a tag instance with 'user'= the user that makes the request.
        Automatically GETS the token authenticated user.
        """
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        """
        Updates a tag instance with 'user'= the user that makes the request.
        Automatically GETS the token authenticated user.
        """
        instance = serializer.save(user=self.request.user)
        return instance


class TagsModelViewset(BaseRecipeAttrsViewSet):
    """
    Handles Tag API requests.
    User must be authenticated to create, read, update, delete.
    """
    queryset = Tag.objects.all()
    serializer_class = RecipeTagSerializer

    def get_queryset(self):
        """
        The queryset is modified to only look for the tags
        the user has created
        """
        query = Tag.objects.filter(user=self.request.user)
        return query


class IngredientsModelViewset(BaseRecipeAttrsViewSet):
    """
    Handles Ingredient API requests.
    User must be authenticated to create, read, update, delete.
    """
    queryset = Ingredient.objects.all()
    serializer_class = RecipeIngredientSerializer

    def get_queryset(self):
        """
        The queryset is modified to only look for the ingredients
        the user has created.
        """
        query = Ingredient.objects.filter(user=self.request.user)
        return query


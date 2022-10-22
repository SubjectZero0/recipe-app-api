from core.models import Ingredient, Recipe, Tag
from .serializers import RecipeSerializer, RecipeTagSerializer, RecipeIngredientSerializer
from .permissions import UpdateMyRecipesPermissions

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet

# Create your views here.

class BaseRecipeViewSet(ModelViewSet):
    """
    Base Viewset for Recipe API.
    """
    queryset = Recipe.objects.all()#Users can GET all recipes
    serializer_class = RecipeSerializer
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

class RecipeApiViewset(BaseRecipeViewSet):
    """
    Handles All Recipe API requests.
    Inherits from BaseRecipeViewSet.
    User has to be authenticated to create update and delete.
    User can only update and delete the recipes they have created.
    """
    #User has to be authenticated to create. They can only update their own recipes
    permission_classes = [IsAuthenticatedOrReadOnly, UpdateMyRecipesPermissions]

class MyRecipesApiViewset(BaseRecipeViewSet):
    """
    Handles My Recipe API requests.
    Inherits from BaseRecipeViewSet.
    User has to be authenticated and can only GET their own recipes.
    User has to be authenticated to create update and delete.
    User can only update and delete the recipes they have created.
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
    Inherits from BaseRecipeAttrsViewSet.
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
    Inherits from BaseRecipeAttrsViewSet.
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


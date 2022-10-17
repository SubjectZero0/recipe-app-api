from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.models import Recipe, Tag



RECIPE_LIST_URL = reverse('recipes-list')
MY_RECIPE_LIST_URL = reverse('my_recipes-list')
TAGS_LIST_URL = reverse('tags-list')

def create_user(**params):
    """Helper function to create a user with variable parameters"""

    user = get_user_model().objects.create_user(**params)
    return user


def create_recipe(user, **params):
    """Helper function to create a recipe with variable users and parameters"""

    recipe = Recipe.objects.create(user=user, **params)
    return recipe


class PublicRecipeApiTests(APITestCase):
    """
    Tests for the 'Recipes' API Public requests
    """

    def setUp(self):
        """
        Creates a user
        """
        user_details = {
            'email' : 'user@example.com',
            'name' : 'user two',
            'password' : 'testpass2'
        }

        create_user(**user_details)

        return super().setUp()

    def test_GET_all_recipes(self):
        """
        Tests if all recipes can be retrieved by anyone
        """
        response = self.client.get(RECIPE_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_recipe_unauthenticated_user(self):
        """
        Tests if unauthenticated users can create a recipe
        """
        payload = {
        'recipe_title':'Test Recipe',
        'recipe_description':'Test description',
        'recipe_instructions':"test instructions",
        }
        response = self.client.post(RECIPE_LIST_URL,payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_recipe_unauthenticated_user(self):
        """
        Tests if unauthorized users can update a recipe
        """
        #for testing purposes, authenticates a user and creates a recipe
        recipe_details = {
        'recipe_title':'Test Recipe',
        'recipe_description':'Test description',
        'recipe_instructions':"test instructions",
        }
        user = get_user_model().objects.get(email='user@example.com')
        self.client.force_authenticate(user)
        recipe = create_recipe(user, **recipe_details)

        self.client.force_authenticate()#un-authenticates user
        RECIPE_DETAIL_URL = reverse('recipes-detail', kwargs={'pk':recipe.id})#Access the recipe detail

        payload = {
            'recipe_title':'New Test Recipe'
        }

        response = self.client.patch(RECIPE_DETAIL_URL, payload)#attempt to patch the recipe

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_recipe_unauthenticated_user(self):
        """
        Tests if unauthorized users can delete a recipe
        """

        #for testing purposes, authenticates a user and creates a recipe
        recipe_details = {
        'recipe_title':'Test Recipe',
        'recipe_description':'Test description',
        'recipe_instructions':"test instructions",
        }
        user = get_user_model().objects.get(email='user@example.com')
        self.client.force_authenticate(user)
        recipe = create_recipe(user, **recipe_details)

        self.client.force_authenticate()#un-authenticates user

        RECIPE_DETAIL_URL = reverse('recipes-detail', kwargs={'pk':recipe.id})#Access the recipe detail
        response = self.client.delete(RECIPE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

############################################################################################################################

class PublicMyRecipeApiTests(APITestCase):
    """
    Tests for the 'My Recipes' API Public requests
    """
    def setUp(self):
        """
        Creates a user, authenticates them,
        creates a recipe and un-authenticates user
        """
        user_details = {
            'email' : 'user@example.com',
            'name' : 'user two',
            'password' : 'testpass2'
        }

        self.user = create_user(**user_details)

        self.client.force_authenticate(self.user)

        recipe_details = {
        'recipe_title':'Test Recipe',
        'recipe_description':'Test description',
        'recipe_instructions':"test instructions",
        }

        self.recipe = create_recipe(self.user, **recipe_details)
        self.client.force_authenticate()

        return super().setUp()

    def test_GET_my_recipe_unauthenticated_user(self):
        """
        Tests if unauthenticated user can retrieve their recipes
        """
        response = self.client.get(MY_RECIPE_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#############################################################################################################################################
class PrivateRecipeApiTests(APITestCase):
    """
    Tests authenticated user Recipe API requests
    """
    def setUp(self):
        """
        Creates a user, authenticates them
        and creates a recipe
        """
        user_details = {
            'email' : 'user@example.com',
            'name' : 'user two',
            'password' : 'testpass2'
        }

        self.user = create_user(**user_details)

        self.client.force_authenticate(self.user)

        recipe_details = {
        'recipe_title':'Test Recipe',
        'recipe_description':'Test description',
        'recipe_instructions':"test instructions",

        }

        self.recipe = create_recipe(self.user, **recipe_details)


        return super().setUp()

    def test_create_recipe(self):
        """
        Tests if authenticated user can create a recipe
        """

        payload = {
        'recipe_title':'Test Recipe 2',
        'recipe_description':'Test description2',
        'recipe_instructions':"test instructions 2"
        }

        response = self.client.post(RECIPE_LIST_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)

    def test_update_recipe(self):
        """
        Tests if authenticated user can patch a recipe they made
        """

        RECIPE_DETAIL_URL = reverse('recipes-detail', kwargs={'pk':self.recipe.id})

        payload = {
            'recipe_title' : 'New Test Recipe'
        }

        response = self.client.patch(RECIPE_DETAIL_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['recipe_title'], 'New Test Recipe')

    def test_update_other_users_recipe(self):
        """
        Tests that an authenticated user
        cannot update another user's recipe
        """
        user_details = {
            'email' : 'user1@example.com',
            'name' : 'user 1',
            'password' : 'testpass1'
        }

        user_1 = create_user(**user_details)#create user_1
        self.client.force_authenticate()#unauthenticate self.user

        self.client.force_authenticate(user_1)#authenticate user_1

        payload = {
            'recipe_title': 'Unauthenticated Patch'
        }

        RECIPE_DETAIL_URL = reverse('recipes-detail', kwargs={'pk':self.recipe.id})#get the recipe detail that belongs to self.user
        response = self.client.patch(RECIPE_DETAIL_URL, payload)#as user_1 try to patch the self.user's recipe
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_recipe(self):
        """
        Tests that an authenticated user
        can delete a recipe they made
        """
        RECIPE_DETAIL_URL = reverse('recipes-detail', kwargs={'pk':self.recipe.id})

        response = self.client.delete(RECIPE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_users_recipe(self):
        """
        Tests that an authenticated user cannot
        delete another user's recipe
        """
        user_details = {
            'email' : 'user1@example.com',
            'name' : 'user 1',
            'password' : 'testpass1'
        }

        user_1 = create_user(**user_details)#create user_1
        self.client.force_authenticate()#unauthenticate self.user

        self.client.force_authenticate(user_1)#authenticate user_1

        RECIPE_DETAIL_URL = reverse('recipes-detail', kwargs={'pk':self.recipe.id})#get the recipe detail that belongs to self.user
        response = self.client.delete(RECIPE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_recipe_with_tags(self):
        """
        Tests creating a recipe instance with tags.
        Tests if the tag also gets created in the Tag API.
        """
        payload = {
        'recipe_title':'Testing Recipe',
        'recipe_description':'Test description',
        'recipe_instructions':"test instructions",
        'tags':[{'tag_name':'Vegeterian'}, {'tag_name':'French'}]
        }

        response = self.client.post(MY_RECIPE_LIST_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(recipe_title = 'Testing Recipe')
        RECIPE_DETAIL_URL = reverse('recipes-detail', kwargs={'pk':recipe.id})
        response = self.client.get(RECIPE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Vegeterian')
        self.assertContains(response, 'French')

        response = self.client.get(TAGS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['tag_name'], 'Vegeterian')
        self.assertEqual(response.data[1]['tag_name'], 'French')

#########################################################################################################################################################

class PrivateMyRecipeApiTests(APITestCase):
    """
    Tests authenticated user's My_Recipes API requests
    """
    def setUp(self):
        """
        Creates a user, authenticates them
        and creates a recipe
        """
        user_details = {
            'email' : 'user@example.com',
            'name' : 'user one',
            'password' : 'testpass'
        }

        self.user = create_user(**user_details)

        self.client.force_authenticate(self.user)

        recipe_details = {
        'recipe_title':'Test Recipe',
        'recipe_description':'Test description',
        'recipe_instructions':"test instructions",
        }

        self.recipe = create_recipe(self.user, **recipe_details)
        return super().setUp()

    def test_GET_My_Recipes(self):
        """
        Tests if an authenticated user can
        retrieve their recipes only
        """
        response = self.client.get(MY_RECIPE_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, 'Test Recipe',)

    def test_GET_other_users_My_Recipes(self):
        """
        Tests that an authenticated user will not
        be able to retrieve another user's recipes
        from My_Recipe API
        """
        user_details = {
            'email' : 'user2@example.com',
            'name' : 'user one',
            'password' : 'testpass'
        }

        self.client.force_authenticate()

        user_2 = create_user(**user_details)

        self.client.force_authenticate(user_2)

        MY_RECIPE_DETAIL_URL = reverse('my_recipes-detail', kwargs={'pk':self.recipe.id})
        response = self.client.get(MY_RECIPE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_my_recipe(self):
        """
        Tests if authenticated user can patch my_recipe, recipe
        """
        MY_RECIPE_DETAIL_URL = reverse('my_recipes-detail', kwargs={'pk':self.recipe.id})
        payload = {
            'recipe_title' : 'New Test Recipe'
        }
        response = self.client.patch(MY_RECIPE_DETAIL_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['recipe_title'], 'New Test Recipe')

    def test_delete_my_recipe(self):
        """
        Tests that an authenticated user
        can delete a my_recipe recipe
        """
        MY_RECIPE_DETAIL_URL = reverse('my_recipes-detail', kwargs={'pk':self.recipe.id})

        response = self.client.delete(MY_RECIPE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_my_recipe_with_tags(self):
        """
        Tests creating a my_recipe instance with tags.
        Tests if the tag also gets created in the Tag API.
        """
        payload = {
        'recipe_title':'Test Recipe3',
        'recipe_description':'Test description3',
        'recipe_instructions':"test instructions3",
        'tags':[{'tag_name':'vegan'}, {'tag_name':'Chinese'}]
        }

        response = self.client.post(MY_RECIPE_LIST_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(recipe_title = 'Test Recipe3')
        MY_RECIPE_DETAIL_URL = reverse('my_recipes-detail', kwargs={'pk':recipe.id})
        response = self.client.get(MY_RECIPE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'vegan')
        self.assertContains(response, 'Chinese')

        response = self.client.get(TAGS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['tag_name'], 'vegan')
        self.assertEqual(response.data[1]['tag_name'], 'Chinese')


    def test_update_my_recipe_with_tags(self):
        """
        Tests updating tags in a recipe.
        Tests if new tag is created in Tag API.
        """
        payload = {
        'recipe_title':'Test Recipe4',
        'recipe_description':'Test description4',
        'recipe_instructions':"test instructions4",
        'tags':[{'tag_name':'vegan'}, {'tag_name':'Chinese'}]
        }

        self.client.post(MY_RECIPE_LIST_URL, payload, format='json')
        recipe = Recipe.objects.get(recipe_title='Test Recipe4')
        MY_RECIPE_DETAIL_URL = reverse('my_recipes-detail', kwargs={'pk':recipe.id})



        payload = {
            'tags' : [{'tag_name':'Vegeterian'}, {'tag_name':'Chinese'}]
        }

        response = self.client.patch(MY_RECIPE_DETAIL_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Vegeterian')
        self.assertContains(response, 'Chinese')
        self.assertEqual(recipe.tags.count(), 2)

        response = self.client.get(TAGS_LIST_URL)
        self.assertContains(response, 'Vegeterian')
from core.models import Ingredient
from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from django.contrib.auth import get_user_model


INGR_LIST_URL = reverse('ingredients-list')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class IngredientsApiTests(APITestCase):
    """
    Tests Ingredient API functionality
    """
    def setUp(self):

        user_details = {
            'email':'testuser@example.com',
            'name':'test name',
            'password':'testpass123'
        }

        self.user = create_user(**user_details)
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredient_list(self):
        """
        Tests retrieving the list of ingredients.
        """
        response = self.client.get(INGR_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ingredient(self):
        """
        Tests creating ingredients.
        """
        payload = {
            'ingredient_name':'Tomatoes'
        }

        response = self.client.post(INGR_LIST_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset({'ingredient_name':'Tomatoes'}, response.data)
        self.assertEqual(response.data['id'], self.user.id)

    def test_patch_ingredient(self):
        """
        Tests patching an ingredient.
        """
        ingr_details = {
            'ingredient_name':'Beef'
        }
        ingredient = Ingredient.objects.create(user=self.user, **ingr_details)
        INGR_DETAIL_URL = reverse('ingredients-detail', kwargs={'pk' : ingredient.id})

        payload = {
            'ingredient_name':'Chicken'
        }
        response = self.client.patch(INGR_DETAIL_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Chicken')

        response = self.client.get(INGR_DETAIL_URL)
        self.assertNotContains(response, 'Beef')
        self.assertContains(response, 'Chicken')

    def test_delete_ingredient(self):
        """
        Tests deleting an ingredient
        """
        ingr_details = {
            'ingredient_name':'Beef'
        }
        ingredient = Ingredient.objects.create(user=self.user, **ingr_details)
        INGR_DETAIL_URL = reverse('ingredients-detail', kwargs={'pk' : ingredient.id})

        response = self.client.delete(INGR_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(INGR_LIST_URL)
        self.assertEqual(len(response.data), 0)

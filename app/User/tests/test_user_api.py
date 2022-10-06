from unittest import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status

CREATE_USER_URL = reverse('User:create') #sets up the url for creating a user

def create_user(**params):
    """Helper function to create a user with variable parameters"""

    user = get_user_model().objects.create_user(**params)
    return user


class PublicUserApiTests(TestCase):
    """Tests Public User API functionalities"""

    def setUp(self):
        """Sets up the client to be the APIClient"""

        self.client = APIClient()

        return super().setUp()

    def test_create_user_success(self):
        """Tests that a user is created and stored successfully in the database"""

        payload = {'email':'user@example.com',
                    'name':'test name',
                    'password':'testpassword'}

        response = self.client.post(CREATE_USER_URL, payload) #creates a response for creating a user at the endpoint

        self.assertEqual(response.status_code, status.HTTP_201_CREATED) #checks the status code of the response

        user = get_user_model().objects.get(email=payload['email']) #GETS user by email
        self.assertEqual(user.check_password, payload['password']) #checks that the hashed user passord translates to the given password

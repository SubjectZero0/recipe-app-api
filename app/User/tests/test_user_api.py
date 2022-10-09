from django.test import Client
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.serializers import ValidationError


USER_URL = reverse('users-list') #sets up the url for creating a user
LOGIN_URL = reverse('User:login')
USER_DETAIL_URL = reverse('users-detail', kwargs={'pk':1})

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

        response = self.client.post(USER_URL, payload) #creates a response for creating a user at the endpoint
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) #checks the status code of the response

        user = get_user_model().objects.get(email=payload['email']) #GETS user by email
        self.assertTrue(user.check_password) #checks that the hashed user passord translates to the given password


    def test_user_with_email_already_exists(self):
        """Tests that email is unique"""

        payload = {'email':'user@example.com',
                    'name':'test name',
                    'password':'testpassword'}

        create_user(**payload)

        response = self.client.post(USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_authentication(self):
        """
        Tests if a user can be authenticated
        and if an auth token is generated

        """
        user_details = {
            'email':'user@example.com',
            'name':'test name',
            'password':'testpassword'
            }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password' : user_details['password']
        }

        response = self.client.post(LOGIN_URL, payload) #attempts to log in

        self.assertEqual(response.status_code, status.HTTP_200_OK)#checks that user was logged in succesfully
        self.assertIn('token', response.data) #checks if there is an auth token in the response data after logging in

    def test_user_no_email_authentication(self):
        """
        Test if a user is authenticated without email

        """
        user_details = {
            'email':'user@example.com',
            'name':'test name',
            'password':'testpassword'
            }

        create_user(**user_details)

        payload = {
            'email': 'asda',
            'password' : user_details['password']
        }

        response = self.client.post(LOGIN_URL, payload) #attempts to log in
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_no_password_authentication(self):
        """
        Tests if a user is authenticated without password
        """
        user_details = {
            'email':'user@example.com',
            'name':'test name',
            'password':'testpassword'
            }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password' : ''
        }

        response = self.client.post(LOGIN_URL, payload) #attempts to log in
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


##############################################################################################


class InactiveUserApiTests(TestCase):
    """
    creates a superuser and sets is_active = False then tests if inactive users
    can log in.
    """

    def setUp(self):
        """
        Sets up the superuser creation, mocks loging in to the django admin page,
        through the Client() client, sets permissions attributes to false,
        saves the changes, and logs out. Finally sets the client to the APIClient()


        """
        self.superuser = get_user_model().objects.create_superuser(
            email = 'testadmin@admin.com',
            name = 'test admin',
            password = 'testpassadmin'
        )

        self.client = Client()
        self.client.login(email = self.superuser.email, password = self.superuser.password)

        self.superuser.is_superuser = False
        self.superuser.is_staff = False
        self.superuser.is_active = False
        self.superuser.save()


        self.client.logout()
        self.client = APIClient()

        return super().setUp()

    def test_user_is_not_active(self):
        """Tests if the superuser is_active is false"""

        user = get_user_model().objects.get(email = 'testadmin@admin.com')
        self.assertFalse(user.is_active)


    def test_user_not_active_authentication_error(self):
        """Tests if the inactive superuser can authenticate to the API"""

        payload = {
            'email' : 'testadmin@admin.com',
            'password' : 'testpassadmin'
        }

        response = self.client.post(LOGIN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)


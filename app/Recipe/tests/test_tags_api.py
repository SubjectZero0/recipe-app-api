from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.models import Tag
from django.urls import reverse
from rest_framework import status

TAG_LIST_URL = reverse('tags-list')


def create_user(**params):
    """Creates a user."""
    user = get_user_model().objects.create_user(**params)
    return user

def create_tag(user, **params):
    """Creates a Tag."""
    tag = Tag.objects.create(user=user, **params)
    return tag

class PublicTagApiTests(APITestCase):
    """Tests Tag API unauthenticated requests."""

    def test_GET_tag_list_unauthenticated_user(self):
        """
        Tests that an unauthenticated user cannot
        retrieve the list of tags.
        """
        response = self.client.get(TAG_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateTagApiTests(APITestCase):
    """
    Tests Tag API authenticated requests.
    """

    def setUp(self):
        """
        Creates a user and authenticates them
        """

        user_details = {
            'email' : 'test@example.com',
            'name': 'test name',
            'password' : 'testpass'
        }
        self.user = create_user(**user_details)
        self.client.force_authenticate(user=self.user)

    def test_GET_tag_list(self):
        """
        Tests that a user can retrieve their
        tag list.
        """
        response = self.client.get(TAG_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tag(self):
        """
        Tests that a user can create a Tag.
        """
        payload = {
            'tag_name' : 'LOLwut?'
        }
        response = self.client.post(TAG_LIST_URL, payload, format='json')
        tag = Tag.objects.get(tag_name = 'LOLwut?')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,{'id':tag.id, 'tag_name': tag.tag_name})

    def test_updating_tag(self):
        """
        Tests updating a tag.
        """
        tag_details = {
            'tag_name':'master tag'
        }
        tag = create_tag(user=self.user, **tag_details)
        TAG_DETAIL_URL = reverse('tags-detail', kwargs={'pk':tag.id})

        payload = {
            'tag_name':'new master tag'
        }
        response = self.client.patch(TAG_DETAIL_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,{'id':tag.id, 'tag_name': payload['tag_name']})

    def test_delete_tag(self):
        """
        Tests deleting a tag.
        """
        tag_details = {
            'tag_name':'delete this tag'
        }
        tag = create_tag(user=self.user, **tag_details)
        TAG_DETAIL_URL = reverse('tags-detail', kwargs={'pk':tag.id})

        response = self.client.delete(TAG_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(tag_name='delete this tag').exists())

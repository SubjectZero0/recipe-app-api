from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Tests models"""

    def test_create_user_with_email_success(self):
        """Test if the user instance creation is succesfull"""

        email = 'test@example.com'
        name = 'test name'
        password = 'testpassword'

        user = get_user_model().objects.create_user(email = email,
                                                    name = name,
                                                    password = password,)

        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))


    def test_create_superuser_with_email_success(self):
        """Test if the superuser instance creation is succesfull"""

        email = 'test2@example.com'
        name = 'test name 2'
        password = 'testpassword2'

        user = get_user_model().objects.create_superuser(email = email,
                                                        name = name,
                                                        password = password,)

        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)

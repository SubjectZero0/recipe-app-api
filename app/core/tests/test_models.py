from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserModelTests(TestCase):
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


    def test_password_hashing(self):
        """Tests if the password provided by the user is the same after creation,
        or it gets hashed."""

        email = 'test3@example.com'
        name = 'test name 3'
        password = 'testpassword3'

        user = get_user_model().objects.create_user(email = email,
                                                    name = name,
                                                    password = password,)
        self.assertNotEqual(user.password, password)


    def test_create_user_without_email(self):
        """Tests if user can be created without email, or it raises a ValueError"""

        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(email = '',
                                                        name = 'test name 4',
                                                        password = 'testpassword4')
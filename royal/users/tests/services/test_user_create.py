from django.core.exceptions import ValidationError
from django.test import TestCase

from royal.users.models import BaseUser
from royal.users.services import user_create


class UserCreateTests(TestCase):
    def test_user_without_password_is_created_with_unusable_one(self):
        user = user_create(email="onderi@gmail.com")

        self.assertFalse(user.has_usable_password())
    
    def test_user_with_capitalized_email_cannot_be_created(self):
        user = user_create(email="onderi@gmail.com")

        with self.assertRaises(ValidationError):
            user_create(email="ONderi@gmail.com")
        
        self.assertEqual(1, BaseUser.objects.count())
    
    def test_create_user_with_password(self):
        user = user_create(email='password@example.com', password='securepassword')
        self.assertEqual(user.email, 'password@example.com')
        self.assertTrue(user.check_password('securepassword')) 
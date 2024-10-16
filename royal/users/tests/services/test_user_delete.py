from django.test import TestCase

from royal.users.models import BaseUser
from royal.users.services import delete_user


class UserDeleteTests(TestCase):
    def setUp(self):
        self.user = BaseUser.objects.create_user(
            email='test@example.com',
            password='securepassword'
    )

    def test_delete_user_success(self):
        self.assertTrue(BaseUser.objects.filter(id=self.user.id).exists())

        delete_user(user_id=self.user.id)

        self.assertFalse(BaseUser.objects.filter(id=self.user.id).exists())
    
    def test_delete_non_existent_user(self):
        with self.assertRaises(BaseUser.DoesNotExist):
            delete_user(user_id=45858)
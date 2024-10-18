from django.test import TestCase

from royal.users.models import BaseUser
from royal.users.services import user_update


class UserUpdateTests(TestCase):
    def setUp(self):
        self.user = BaseUser.objects.create_user(email="onderi@gmail.com", first_name='Test', last_name='User')

    def test_first_last_name_string(self):
        data = {
            "first_name": "onderi",
            "last_name": "updated"
        }

        user = user_update(user_id=self.user.id, data=data)

        self.assertEqual(user.first_name, "onderi")
        self.assertEqual(user.last_name, "updated")
  

from datetime import timedelta
from unittest.mock import  Mock, patch

from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

from royal.common.factories import RandomModelFactory,SimpleModelFactory
from royal.common.services import model_update

# class ModelUpdateTests(TestCase):
#     def setUp(self):
#         self.model_instance = RandomModelFactory()
#         self.simple_object = SimpleModelFactory()
#         self.instance = Mock(field_a=None, field_b=None, field_c=None)

#     def test_model_update_does_nothing(self):
#         with self.subTest("when no fields are provided"):
#             instance = RandomModelFactory()

#             updated_instance, has_updated = model_update(instance=instance, fields=[], data={})

#             self.assertEqual(instance, updated_instance)
#             self.assertFalse(has_updated)
#             self.assertNumQueries(0)

#         with self.subTest("when non of the fields are in the data"):
#             instance = RandomModelFactory()

#             updated_instance, has_updated = model_update(instance=instance, fields=["start_date"], data={"foo": "bar"})

#             self.assertEqual(instance, updated_instance)
#             self.assertFalse(has_updated)
#             self.assertNumQueries(0)


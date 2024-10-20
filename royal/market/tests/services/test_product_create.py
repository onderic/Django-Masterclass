from django.core.exceptions import ValidationError
from django.test import TestCase
from royal.market.models import Product
from royal.market.services import product_create


class ProductCreateTests(TestCase):
    def setUp(self):
        self.product_data = {
            "name": "shoes",
            "description": "desc",
            "price": 122.33,
            "stock": 5
        }
    
    def test_product_creation(self):
        product = product_create(**self.product_data)

        self.assertIsInstance(product, Product)
        self.assertEqual(product.name, self.product_data["name"])
        self.assertEqual(product.description, self.product_data["description"])
        self.assertEqual(product.price, self.product_data["price"])
        self.assertEqual(product.stock, self.product_data["stock"])
    

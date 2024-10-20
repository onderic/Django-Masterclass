from django.test import TestCase
from django.core.exceptions import ValidationError
from django.http import Http404
from royal.market.models import Product
from royal.market.services import product_update


class ProductUpdateTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=100.00,
            stock=10,
        )
    
    def test_product_not_founf(self):
        data = {
            "name": "Non-existent Product",
            "description": "No Description",
            "price": 200.00,
            "stock": 5,
        }

        with self.assertRaises(Http404):
            product_update(product_id=10999999999999999999991, data=data)
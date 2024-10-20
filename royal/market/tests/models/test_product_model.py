from django.test import TestCase
from django.utils import timezone
from royal.market.models import Product
from datetime import timedelta

class ProductModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="A test product.",
            price=100.00,
            stock=10
        )

    def test_is_in_stock(self):
        self.assertTrue(self.product.is_in_stock())
        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.is_in_stock())
    
    def test_decrease_stock_success(self):
        self.assertTrue(self.product.decrease_stock(5))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)
    
    def test_decrease_stock_failure(self):
        self.assertFalse(self.product.decrease_stock(15))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)
    
    def test_increase_stock(self):
        self.product.increase_stock(5)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 15)
    
    def test_was_added_recently(self):
        self.assertTrue(self.product.was_added_recently())

        old_product = Product.objects.create(
            name="Old Product",
            description="An older product.",
            price=50.00,
            stock=5
        )

        old_product.created_at = timezone.now() - timedelta(days=8)
        old_product.save()

        self.assertFalse(old_product.was_added_recently())
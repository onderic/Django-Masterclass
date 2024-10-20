from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from royal.market.models import Order, OrderItem, Product
from royal.users.models import BaseUser
from royal.market.services import create_order


class CreateOrderTests(TestCase):
    def setUp(self):
        self.user = BaseUser.objects.create(email="onderi@gmail.com", password="12334567")

        self.product1 = Product.objects.create(name='Product 1', price=50.00, stock=10)
        self.product2 = Product.objects.create(name='Product 2', price=30.00, stock=5)

    def test_create_order_success(self):
        order_items_data = [
           { "product": self.product1.id, "quantity": 2},
           { "product": self.product2.id, "quantity": 2},
        ]
        
        order = create_order(self.user, order_items_data)

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.order_items.count(), 2)
        self.assertEqual(order.total_price, 160.00)

        self.product1.refresh_from_db()
        self.product2.refresh_from_db()

        self.assertEqual(self.product1.stock, 8)
        self.assertEqual(self.product2.stock, 3)
        

    def test_create_order_insufficient_stock(self):
        order_items_data = [
           { "product": self.product1.id, "quantity": 288},
        ]

        with self.assertRaises(ValidationError) as context:
            create_order(self.user, order_items_data)
        
        self.assertIn("Error adding item Product 1", str(context.exception))

        self.assertFalse(Order.objects.filter(user=self.user).exists())

        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock, 10)


    def test_create_order_atomicity(self):
        order_items_data = [
           { "product": self.product1.id, "quantity": 2},
           { "product": self.product2.id, "quantity": 122},
        ]

        with self.assertRaises(ValidationError):
            create_order(self.user, order_items_data)

        self.assertFalse(Order.objects.filter(user=self.user).exists())

        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock, 10)
        self.assertEqual(self.product2.stock, 5)
from django.test import TestCase
from royal.market.models import Order, OrderItem, Product
from royal.users.models import BaseUser

class OrderModelTests(TestCase):
    def setUp(self):
        self.user = BaseUser.objects.create(email="onderi@gmail.com", password="12334567")

        self.product = Product.objects.create(name="product1", price=10.00, stock=10)

        self.order = Order.objects.create(user=self.user)

    def test_calculate_total(self):
        OrderItem.objects.create(order=self.order, product=self.product, quantity=2, total_price=20.00),
        OrderItem.objects.create(order=self.order, product=self.product, quantity=2, total_price=20.00),

        self.order.calculate_total()
        self.order.refresh_from_db()

        self.assertEqual(self.order.total_price, 40.00)
    
    def test_mark_as_completed(self):
        self.order.mark_as_completed()
        self.order.refresh_from_db()

        self.assertEqual(self.order.status, Order.OrderStatus.COMPLETED)
    
    def test_cancel_order(self):
        self.order.cancel_order()
        self.order.refresh_from_db()

        self.assertEqual(self.order.status, Order.OrderStatus.CANCELLED)
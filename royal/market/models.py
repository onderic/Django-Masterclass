from django.db import models
from django.utils import timezone
from royal.common.models import BaseModel
from django.core.exceptions import ValidationError

class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def is_in_stock(self):
        return self.stock > 0

    def decrease_stock(self, quantity=1):
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            return True
        return False

    def increase_stock(self, quantity=1):
        self.stock += quantity
        self.save()

    def was_added_recently(self):
        return self.created_at >= timezone.now() - timezone.timedelta(days=7)


class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        COMPLETED = 'C', 'Completed'
        CANCELLED = 'X', 'Cancelled'

    user = models.ForeignKey('users.BaseUser', on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=1,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    def calculate_total(self):
        self.total_price = sum(item.total_price for item in self.order_items.all())
        self.save()

    def mark_as_completed(self):
        self.status = self.OrderStatus.COMPLETED
        self.save()

    def cancel_order(self):
        self.status = self.OrderStatus.CANCELLED
        self.save()



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
       
        self.total_price = self.product.price * self.quantity
        
        # Validate stock availability
        if self.quantity > self.product.stock:
            raise ValidationError(f'Not enough stock for product: {self.product.name}')

        # Decrease stock for the product being ordered
        self.product.decrease_stock(self.quantity)

        super().save(*args, **kwargs)

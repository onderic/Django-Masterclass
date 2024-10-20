from rest_framework import serializers
from .models import Order, OrderItem, Product
from royal.users.models import BaseUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['email', 'first_name', 'last_name'] 

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'product_price', 'quantity', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user', 
            'total_price',
            'created_at',
            'updated_at',
            'status',
            'order_items'
        ]
        read_only_fields = ['total_price', 'created_at', 'updated_at', 'status']

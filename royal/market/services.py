from .models import Product,Order,OrderItem
from django.db import transaction
from royal.common.services import model_update
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from royal.users.models import BaseUser



def product_create(*, name: str, description: str = '', price: float, stock: int = 0) -> Product:
    product = Product.objects.create(name=name, description=description, price=price, stock=stock)

    return product


@transaction.atomic
def product_update(*,product_id, data) -> Product:

    product = get_object_or_404(Product, id=product_id)

    non_side_effect_fields = ["name", "description", "price","stock"]

    product, has_updated = model_update(instance=product, fields=non_side_effect_fields, data=data)

    return product


@transaction.atomic
def delete_product(product_id:int) ->  None:
    product = get_object_or_404(Product, id=product_id)
    product.delete()


@transaction.atomic
def create_order(user, order_items_data):
    order = Order(user=user) 
    order.save()

    total_price = 0

    for item_data in order_items_data:
        product_id = item_data.get("product")
        quantity = item_data.get("quantity")

        product = get_object_or_404(Product, id=product_id)

        order_item = OrderItem(order=order, product=product, quantity=quantity)

        try:
            order_item.save()
            total_price += order_item.total_price
        except ValidationError as e:
            raise ValidationError(f"Error adding item {product.name}: {str(e)}")

    order.total_price = total_price
    order.save()

    return order

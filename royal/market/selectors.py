from django.db.models.query import QuerySet

from .filters import ProductFilter, OrderFilter
from .models import Product, Order


def product_list(*, filters=None) -> QuerySet[Product]:
    filters = filters or {}

    qs = Product.objects.all()

    return ProductFilter(filters, qs).qs


def order_list(*, filters=None) -> QuerySet[Order]:
    filters = filters or {}

    qs = Order.objects.all().order_by('-created_at')


    return OrderFilter(filters, qs).qs


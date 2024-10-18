from django.db.models.query import QuerySet

from .filters import ProductFilter
from .models import Product


def product_list(*, filters=None) -> QuerySet[Product]:
    filters = filters or {}

    qs = Product.objects.all()

    return ProductFilter(filters, qs).qs

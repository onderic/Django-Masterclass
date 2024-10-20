import django_filters

from .models import Product,Order

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ("id", "name")


class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()
    updated_at = django_filters.DateTimeFromToRangeFilter()
    status = django_filters.ChoiceFilter(choices=Order.OrderStatus.choices)

    class Meta:
        model = Order
        fields = ("id", "user", "total_price", "created_at", "updated_at", "status")
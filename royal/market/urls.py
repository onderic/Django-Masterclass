from django.urls import path
from .apis import (
    ProductCreateApi,
    ProductListApi,
    UpdateProductApi,
    DeleteProductApi, 
    OrderApi, 
    OrderListApi,
    UserOrderListApi
)

urlpatterns = [
    path("list/", ProductListApi.as_view(), name="product-list"), 
    path("create/", ProductCreateApi.as_view(), name="product-create"),
    path('update/<int:product_id>/', UpdateProductApi.as_view(), name='product-update'),
    path('delete/<int:product_id>/', DeleteProductApi.as_view(), name='product-delete'),

    # orders
    path("order/create/", OrderApi.as_view(), name="order-create"),
    path("order/list/", OrderListApi.as_view(), name="order-list"),
    path("order/user/list/", UserOrderListApi.as_view(), name="order-list"),

]
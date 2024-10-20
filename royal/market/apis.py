from rest_framework import serializers,status
from rest_framework.views import APIView
from royal.api.mixins import ApiAuthMixin
from royal.api.permissions import IsAdminOrSuperuser
from rest_framework.response import Response
from .serializers import OrderSerializer
from royal.market.models import Product
from .services import (
    product_create,
    product_update,
    delete_product,
    create_order
)
from .selectors import product_list,order_list
from royal.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)


class ProductCreateApi(ApiAuthMixin, APIView):
    permission_classes = [IsAdminOrSuperuser]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        description = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        stock = serializers.IntegerField()
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)



class ProductListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 4

    class FilterSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        description = serializers.CharField(required=False)
        price = serializers.DecimalField(required=False,max_digits=10, decimal_places=2)
        stock = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ("id", "name", "description","price","stock")

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
    
        products = product_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=products,
            request=request,
            view=self
        )


class UpdateProductApi(ApiAuthMixin, APIView):
    
    permission_classes = [IsAdminOrSuperuser]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        description = serializers.CharField(required=False)
        price = serializers.DecimalField(required=False,max_digits=10, decimal_places=2)
        stock = serializers.IntegerField(required=False)

    def post(self, request, product_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = product_update(product_id=product_id, data=serializer.validated_data)

        output_serializer = self.InputSerializer(product)
        
        return Response({"product": output_serializer.data}, status=status.HTTP_200_OK)
    


class DeleteProductApi(ApiAuthMixin, APIView):

    permission_classes = [IsAdminOrSuperuser]

    def delete(self,request, product_id):
        delete_product(product_id=product_id)

        return Response(status=status.HTTP_200_OK)
    

class OrderApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        order_items = serializers.ListField(
            child= serializers.DictField(
                child = serializers.IntegerField()
            ),
            min_length = 1
        )
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_items_data = serializer.validated_data['order_items']
        user = request.user

        order = create_order(user, order_items_data)
        
        return Response(
            {
                "order":order.id,
                "total_amount": order.total_price,
                "created_at": order.created_at

            } ,status=status.HTTP_200_OK)



class OrderListApi(ApiAuthMixin, APIView):
    permission_classes = [IsAdminOrSuperuser] 
    OutputSerializer = OrderSerializer

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    def get(self, request):
        filters_serializer = self.OutputSerializer(data=request.query_params, partial=True)
        filters_serializer.is_valid(raise_exception=True)

        filters = filters_serializer.validated_data
        filters['status'] = 'P'

        orders = order_list(filters=filters)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=orders,
            request=request,
            view=self
        )



class UserOrderListApi(ApiAuthMixin, APIView):
    OutputSerializer = OrderSerializer

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    def get(self, request):
        user = request.user
        filters = {
            'user': user.id, 
            'status': 'P' 
        }

        orders = order_list(filters=filters)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=orders,
            request=request,
            view=self
        )
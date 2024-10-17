from django.shortcuts import get_object_or_404
from rest_framework import serializers,status
from rest_framework.views import APIView
from royal.api.mixins import ApiAuthMixin

from royal.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from royal.users.models import BaseUser
from royal.users.selectors import user_list
from .services import user_create,user_update,delete_user
from rest_framework.response import Response

class UserCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(write_only=True)
        is_active = serializers.BooleanField(default=True)
        is_admin = serializers.BooleanField(default=False)
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 

        user_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserListApi(ApiAuthMixin,APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        is_admin = serializers.BooleanField(required=False, allow_null=True, default=None)
        email = serializers.EmailField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("id", "email", "is_admin","first_name","last_name","jwt_key")

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=users,
            request=request,
            view=self,
        )

class UserUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=False, allow_blank=True)
        last_name = serializers.CharField(required=False, allow_blank=True)

    def post(self, request, user_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(BaseUser, id=user_id)

        updated_user = user_update(user=user, data=serializer.validated_data)

        return Response({
            "email": updated_user.email,
            "firstname": updated_user.first_name,
            "lastname": updated_user.last_name,
        }, status=status.HTTP_200_OK)

class UserDeleteApi(APIView):

    def delete(self, request, user_id):

        user = get_object_or_404(BaseUser, id=user_id)
        delete_user(user_id=user.id)

        return Response(status=status.HTTP_200_OK)
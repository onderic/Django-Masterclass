from django.conf import settings
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebTokenView

from royal.api.mixins import ApiAuthMixin
from royal.authentication.services import auth_logout
from royal.users.selectors import user_get_login_data


class UserJwtLoginApi(ObtainJSONWebTokenView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            response.status_code = status.HTTP_200_OK

        return response


class UserJwtLogoutApi(ApiAuthMixin, APIView):
    def post(self, request):
        auth_logout(request.user)

        response = Response()

        if settings.JWT_AUTH["JWT_AUTH_COOKIE"] is not None:
            response.delete_cookie(settings.JWT_AUTH["JWT_AUTH_COOKIE"])

        return response


class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request):
        data = user_get_login_data(user=request.user)

        return Response(data)

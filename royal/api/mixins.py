from importlib import import_module
from typing import TYPE_CHECKING, Sequence, Type

from django.contrib import auth
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

if TYPE_CHECKING:
    from rest_framework.permissions import _PermissionClass

    PermissionClassesType = Sequence[_PermissionClass]
else:
    PermissionClassesType = Sequence[Type[BasePermission]]


class ApiAuthMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JSONWebTokenAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsAuthenticated,)

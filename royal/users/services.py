from typing import Optional

from django.db import transaction

from royal.common.services import model_update
from .models import BaseUser



def user_create(
    *, email: str, is_active: bool = True, is_admin: bool = False, password: Optional[str] = None
) -> BaseUser:
    user = BaseUser.objects.create_user(email=email, is_active=is_active, is_admin=is_admin, password=password)

    return user

@transaction.atomic
def user_update(*, user: BaseUser, data) -> BaseUser:
    non_side_effect_fields = ["first_name", "last_name"]

    user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

    return user

@transaction.atomic
def delete_user(user_id:int) -> None:
    user = BaseUser.objects.get(id=user_id)

    user.delete()
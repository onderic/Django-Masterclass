from typing import Optional

from django.db import transaction
from django.shortcuts import get_object_or_404

from royal.common.services import model_update
from royal.notifications.models import Email
from .models import BaseUser
from royal.notifications.tasks import email_send



def user_create(*, email: str, is_active: bool = True, is_admin: bool = False, password: Optional[str] = None) -> BaseUser:
    user = BaseUser.objects.create_user(email=email, is_active=is_active, is_admin=is_admin, password=password)

    return user

@transaction.atomic
def user_update(*,user_id, data) -> BaseUser:

    user = get_object_or_404(BaseUser, id=user_id)

    non_side_effect_fields = ["first_name", "last_name"]

    user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

    if has_updated:
        email = Email.objects.create(
            status= Email.Status.READY,
            to=user.email,
            subject="Your profile has been updated",
            html=f"<p>Hello {user.first_name},</p><p>Your profile has been successfully updated.</p>",
            plain_text=f"Hello {user.first_name},\n\nYour profile has been successfully updated."
        )
    email_send.delay(email.id)

    return user



@transaction.atomic
def delete_user(user_id: int) -> None:
    user = get_object_or_404(BaseUser, id=user_id)
    
    user.delete()
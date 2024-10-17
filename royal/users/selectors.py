from django.db.models.query import QuerySet

from .filters import BaseUserFilter
from .models import BaseUser

def user_get_login_data(*, user:BaseUser):
    return{
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
      
    }

def user_list(*, filters=None) -> QuerySet[BaseUser]:
    filters = filters or {}

    qs = BaseUser.objects.all()

    return BaseUserFilter(filters, qs).qs

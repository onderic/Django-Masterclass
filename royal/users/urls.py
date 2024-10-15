from django.urls import path
from .apis import UserListApi,UserCreateApi,UserUpdateApi,UserDeleteApi

urlpatterns = [
    path("list/", UserListApi.as_view(), name="user-list"), 
    path("create/", UserCreateApi.as_view(), name="user-create"),
    path('update/<int:user_id>/', UserUpdateApi.as_view(), name='user-update'),
    path('delete/<int:user_id>/', UserDeleteApi.as_view(), name='user-delete'),
]

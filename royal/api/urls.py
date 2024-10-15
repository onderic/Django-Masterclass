from django.urls import include, path

urlpatterns = [
    path("users/", include(("royal.users.urls", "users"))),
    path("auth/", include(("royal.authentication.urls", "auth"))),

]
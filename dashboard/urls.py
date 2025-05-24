from django.contrib.auth.forms import UserCreationForm
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dashboard.views import UsersViewSet, user_view

router = DefaultRouter()
router.register("users", UsersViewSet, basename="users")

urlpatterns = [
    #     path("", user_view, name="register_page"),
    #     path(
    #         "register/",
    #         user_view,
    #     ),
    #     path(
    #         "login/",
    #         user_view,
    #     ),
]

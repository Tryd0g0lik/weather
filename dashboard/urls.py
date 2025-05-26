from django.contrib.auth.forms import UserCreationForm
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dashboard.views import UsersViewSet, dashboard_view, main_view

router = DefaultRouter()
router.register("index", UsersViewSet, basename="index")
# router.register("0/login_user", UsersViewSet, basename="login_user")
urlpatterns = [
    path("", main_view, name="weather"),
    path("register/", dashboard_view, name="register_page"),
    path("login/", dashboard_view, name="login_page"),
    # path("", include((router.urls, "api"), namespace="api")),
    #     path(
    #         "register/",
    #         user_view,
    #     ),
    #     path({
    #
    #     "password": "ds2Rssa8%sa",
    #     "is_staff": false,
    #     "username": "Victorovich"
    # }
    #         "login/",
    #         user_view,
    #     ),
]
# urlpatterns += router.urls

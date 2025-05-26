"""
project/urls.py

URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import path, include
from dashboard.urls import router as users_router, urlpatterns as dashboard
from weather.urls import router as weather_router, urlpatterns as weather

# from weather.urls import urlpatterns as weather_url

urlpatterns = [
    path("admin/", admin.site.urls),
    path("weather/", include((weather, "weather"), namespace="weather")),
    # path("", include((dashboard, "dashboard"), namespace="dashboard")),
    path("", include((dashboard, "dashboard"), namespace="dashboard")),
    path("api/v1/users/", include((users_router.urls, "users"), namespace="users")),
    path(
        "api/v1/weather/",
        include((weather_router.urls, "weather"), namespace="weather"),
    ),
]

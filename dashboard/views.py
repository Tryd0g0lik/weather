import os
import json
import logging

from asgiref.sync import sync_to_async
from geoip2 import database as location
from datetime import datetime
from typing import TypeVar, Dict
from django.shortcuts import render
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from dashboard.hasher import PassworHasher
from dashboard.models import Users
from django.contrib.auth.base_user import AbstractBaseUser
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from project.settings import BASE_DIR, SECRET_KEY, SIMPLE_JWT
# Create your views here.
from rest_framework_simplejwt.tokens import TokenUser
from logs import configure_logging
configure_logging(logging.INFO)
log = logging.getLogger(__name__)
AuthUser = TypeVar("AuthUser", Users, TokenUser)
def serializer_validate(serializer):
    is_valid = serializer.is_valid()
    if not is_valid:
        log.error("SERIALIZER ERROR: %s", serializer.errors)
        raise serializers.ValidationError(serializer.errors)
    log.info("SERIALIZER DATA VALID", serializer.validated_data)
    
class UsersViewSet(viewsets.ViewSet):
    @action(methods=["POST"], detail=False)
    async def login_user(self, request) -> {Dict[str, str]}:
        """HASHING PASSWORD"""
        password = request.data.get("password")
        login = request.data.get("username")
        hash = PassworHasher()
        salt = SECRET_KEY.replace("$", "/")
        hash_password = hash.hasher(password, salt[:50])
        
        """CHECK EXISTS OF USER"""
        user_list = sync_to_async(Users.objects.filter)(
            username=login, password=hash_password
        )
        if not user_list.exists():
            log.error("USER NOT FOUNDED")
            return Response(
                json.dumps({"data": "User not founded"}),
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        """GET USER DATA"""
        user = user_list[0]
        user.is_active = True
        user.is_anonymous = False
        user.last_login = datetime.now()
        """GET LOCATION OF USER"""
        user_ip_address = request.META.get("REMOTE_ADDR")

        try:
            reader = location.Reader('GeoLite2-City.mmdb')
            response = reader.city(user_ip_address)
            latitude: float = response.location.latitude
            longitude: float = response.location.longitude
            log.info("LATITUDE OF USER: %s", latitude)
            log.info("LONGITUDE OF USER: %s", longitude)
            user.set_latitude = {"latitude": latitude}
            user.set_longitude = {"longitude": longitude}
            """SAVE USER"""
            user.save()
            log.info("USER IS ACTIVE: %s", user.is_active)
            # token = LogingViewSet._jwt_get_token(user)
            """LOGIN USER"""
            log.info("USER FOUND")
            
            token: dict = await self.async_token(user)
            return Response(token, status=status.HTTP_200_OK)
        except Exception as ex:
            log.error("USER ERROR: %s", ex.args)
            return Response(
                json.dumps({"detail": ex.args}),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    @classmethod
    async def async_token(cls, user_object: AuthUser) -> {Dict[str, str]}:
        """
        This is method for getting token for user.
        :param user_object: This is a user's object for a which will be token generating \
        :return: this dictionary with 4 values
        :return: {
                {"token_access": "< access_token >", "live_time": "< life_time_of_token >"},
                {"token_refresh": "< refresh_token >", "live_time": "< life_time_of_token >"}
            }
        """

        tokens = await cls.__async_generate_jwt_token(user_object)
        return tokens

    @classmethod
    async def __async_generate_jwt_token(cls, user_object: AuthUser) -> {Dict[str, str]}:
        """
        Only, after registration user we will be generating token for \
        user through 'rest_framework_simplejwt.serializers.TokenObtainPairSerializer'
        This is a generator token of user.\
        The 'SIMPLE_JWT' is variable from the project's 'settings.py' file.\
        @SIMPLE_JWT.ACCESS_TOKEN_LIFETIME this is minimum quantity for life of token\
         It is for the access.\
        @REFRESH_TOKEN_LIFETIME this is maximum quantity fro life token. \
        It is for the refresh.
        'TokenObtainPairSerializer' it has own db/
        :return:
        """
        """TIME TO THE LIVE TOKEN"""
        # dt = datetime.datetime.now() + datetime.timedelta(days=1)
        """GET TOKEN"""
        try:

            token = await sync_to_async(TokenObtainPairSerializer.get_token)(user_object)
            token["name"] = (lambda : user_object.username)()
            return {
                {"token_access": str(token.access_token), "live_time": SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]},
                {"token_refresh": str(token), "live_time": SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"] }
            }
        except Exception as ex:
            raise ValueError("Value Error: %s" % ex)


def user_view(request):
    # form_reg =UserRegister()
    form = "" # UserLogin()
    # form = AuthenticationForm()
    title = "Вход в аккаунт"
    if "register" in request.path.lower():
        # form = UserCreationForm()
        form = "" #  UserRegisterForm()
        title = "Регистрация"

    files = os.listdir(f"{BASE_DIR}/ads/static/scripts")
    css_file = "styles/index.css"

    return render(
        request,
        "register/index.html",
        {
            "js_files": files,
            "css_file": css_file,
            "form": {
                "form_user": form,
            },
            "title": title,
        },
    )

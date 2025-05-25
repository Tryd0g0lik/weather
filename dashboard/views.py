"""
dashboard/views.py
"""

import os
import json
import logging
import requests
from asgiref.sync import sync_to_async
from datetime import datetime
from typing import TypeVar, Dict
from django.shortcuts import render
from adrf.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, status  # , viewsets
from dashboard.forms.form_login import UserLogin
from dashboard.forms.form_register import UserRegisterForm
from dashboard.hasher import PassworHasher
from dashboard.models import Users
from dashboard.serializers import UsersSerializer
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


class UsersViewSet(ViewSet):
    """
    This is a simple API to create a user and login users\
    This 'create' method is sync view. It has the 'api/v1/users/index/' api key.\
    before, user registration, request's data will be checking for user's duplicate by 'username'.
    If, only 'username' of data request is unique, then it will be created through the serializer.\
    And. 'password' from data request will be hashed before saving.\

    This 'login_user' method is async view. It has the '/api/v1/users/index/0/login_user/' api key.\
    Here, pas
    """

    def create(self, request) -> type(Response):
        """CHECK USER DATA"""
        user = request.user
        salt = SECRET_KEY.replace("$", "/")
        h = PassworHasher()
        password_hash = h.hasher(request.data.get("password"), salt[:50])
        log.info("PASSWORD HASH: %s", password_hash)
        """CHECK USER EXISTS"""
        user_list = Users.objects.filter(username=request.data.get("username"))

        log.info("USER EXISTS: %s", user_list.exists())
        if not user.is_authenticated and not user_list.exists():
            try:
                serializer = UsersSerializer(data=request.data)
                serializer_validate(serializer)
                serializer.validated_data["password"] = password_hash
                serializer.save()
                log.info("USER CREATED SUCCESSFUL")
                return Response(
                    {"data": "USER CREATED"}, status=status.HTTP_201_CREATED
                )

            except Exception as ex:
                log.error("SERIALIZER DATA ERROR: %s", ex.args)
                return Response(
                    {"detail": ex.args}, status=status.HTTP_401_UNAUTHORIZED
                )
        log.error("USER NOT CREATED")
        return Response(
            json.dumps({"detail": "USER NOT CREATED"}),
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @action(methods=["POST"], detail=True)
    async def login_user(self, request, pk: str = "0"):
        """
        This method is used the user's login and IP ADDRESS of client.
        Here, If wwe have the object of user , it means we will  get token objects for user.
        "token_access" - it is general token of user for access to the service.
        "token_refresh" - it is token for refresh the access token.
        :param request:
        :param pk: not used. It is just for URL.
        :return: ```js
        {"data":[
                    {
                        "token_access": str( < access_token >),
                        "live_time": < lifetime_from_minutes >,
                    },
                    {
                        "token_refresh": str(tokens),
                        "live_time": < lifetime_from_hours >,
                    },
                ]}
                ````
        """
        password = request.data.get("password")
        login = request.data.get("username")
        hash = PassworHasher()
        salt = SECRET_KEY.replace("$", "/")
        hash_password = hash.hasher(password, salt[:50])

        """CHECK EXISTS OF USER"""
        user_one = await sync_to_async(Users.objects.filter)(
            username=login, password=hash_password
        )
        user_one = await sync_to_async(user_one.first)()

        if not user_one:
            log.error("USER NOT FOUNDED")
            return Response(
                {"data": "User not founded"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        """GET USER DATA"""
        user_one.is_active = True
        # user_one.is_anonymous = False

        user_one.last_login = datetime.now()
        """GET LOCATION OF USER"""
        user_ip_address = request.META.get("REMOTE_ADDR")  # Не трогать - используется

        try:
            response = await sync_to_async(requests.post)(
                "http://ip-api.com/batch",
                data=json.dumps(
                    [
                        {
                            "query": "83.166.245.197",  # Изменить на user_ip_address
                            "fields": ["lat", "lon"],  # Исправлено на lat/lon
                            "lang": "ru",
                        }
                    ]
                ),
            )
            response = response.json()
            """GET LOCATION BASIS/INITIAL"""
            latitude: float = response[0]["lat"]
            longitude: float = response[0]["lon"]
            log.info("LATITUDE OF USER: %s", latitude)
            user_one.latitude = latitude
            user_one.longitude = longitude
            """SAVE USER"""
            await sync_to_async(user_one.save)()
            log.info("USER IS ACTIVE: %s", user_one.is_active)
            tokens = await self.async_token(user_one)
            log.info("USER TOKEN IS ACTIVE: %s", str(tokens))
            return Response(
                {
                    "data": [
                        {
                            "token_access": str(tokens.access_token),
                            "live_time": SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                        },
                        {
                            "token_refresh": str(tokens),
                            "live_time": SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                        },
                    ]
                },
                status=status.HTTP_200_OK,
            )
        except Exception as ex:
            log.error("USER ERROR: %s", ex.args)
            return Response({"detail": ex.args}, status=status.HTTP_401_UNAUTHORIZED)

    @classmethod
    async def async_token(cls, user_object: AuthUser):
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

    @staticmethod
    async def __async_generate_jwt_token(user_object: AuthUser) -> {Dict[str, str]}:
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
            token = TokenObtainPairSerializer.get_token(user_object)
            token["name"] = (lambda: user_object.username)()
            return token
        except Exception as ex:
            raise ValueError("Value Error: %s" % ex)


def dashboard_view(request):

    form = UserLogin()
    # form = AuthenticationForm()
    title = "Вход в аккаунт"
    if "register" in request.path.lower():
        # form = UserCreationForm()
        form = UserRegisterForm()
        title = "Регистрация"

    files = os.listdir(f"{BASE_DIR}/weather/static/scripts")
    css_file = "styles/index.css"

    return render(
        request,
        "users/index.html",
        {
            "js_files": files,
            "css_file": css_file,
            "title": title,
            "form": {
                "form_user": form,
            },
        },
    )

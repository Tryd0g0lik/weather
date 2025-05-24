"""
dashboard/models.py
"""
import datetime
from typing import Dict
from asgiref.sync import sync_to_async
# from django.contrib.auth.base_user import AbstractBaseUser
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.exceptions import InvalidToken
# from rest_framework_simplejwt.tokens import TokenUser
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator
)
from project.settings import SIMPLE_JWT
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Users(AbstractUser):
    latitude = models.FloatField(
        max_length=7,
        blank=True,
        default=0.0,
        help_text=_("latitude for forecast"),
        validators = [
            MaxLengthValidator(
                7,
                message=_("Maximum quantity of symbols before 7 symbols/characters")
            ),
            MinLengthValidator(
                2,
                message=_("Minimum quantity of symbols is 2 symbols/characters")
            )
        ]
    )
    longitude = models.FloatField(
        max_length=7,
        blank=True,
        default=0.0,
        help_text=_("longitude for forecast"),
        validators = [
            MaxLengthValidator(
                7,
                message=_("Maximum quantity of symbols before 7 symbols/characters")
            ),
            MinLengthValidator(
                2,
                message=_("Minimum quantity of symbols is 2 symbols/characters")
            )
        ]
    )

    def __str__(self):
        return "Latitude: %s. Latitude: %s" % (self.latitude, self.latitude)
    class Meta:
        db_table = "users"
        # fields = ["username", "latitude", "longitude", "ix_active", "last_name", ]
    # @property
    # async def async_token(self) -> {Dict[str, str]}:
    #     """
    #     This is method for getting token for user.
    #     :return: this dictionary with 4 values
    #     :return: {
    #             {"token_access": "< access_token >", "live_time": "< life_time_of_token >"},
    #             {"token_refresh": "< refresh_token >", "live_time": "< life_time_of_token >"}
    #         }
    #     """
    #     tokens = await self.__async_generate_jwt_token()
    #     return tokens
    #
    # async def __async_generate_jwt_token(self) -> {Dict[str, str]}:
    #     """
    #     Only, after registration user we will be generating token for \
    #     user through 'rest_framework_simplejwt.serializers.TokenObtainPairSerializer'
    #     This is a generator token of user.\
    #     The 'SIMPLE_JWT' is variable from the project's 'settings.py' file.\
    #     @SIMPLE_JWT.ACCESS_TOKEN_LIFETIME this is minimum quantity for life of token\
    #      It is for the access.\
    #     @REFRESH_TOKEN_LIFETIME this is maximum quantity fro life token. \
    #     It is for the refresh.
    #     'TokenObtainPairSerializer' it has own db/
    #     :return:
    #     """
    #     """TIME TO THE LIVE TOKEN"""
    #     # dt = datetime.datetime.now() + datetime.timedelta(days=1)
    #     """GET TOKEN"""
    #     try:
    #         token = await sync_to_async(TokenObtainPairSerializer.get_token)(self)
    #         token["name"] = (lambda : self.username)()
    #         return {
    #             {"token_access": str(token.access_token), "live_time": SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]},
    #             {"token_refresh": str(token), "live_time": SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"] }
    #         }
    #     except Exception as ex:
    #         raise ValueError("Value Error: %s" % ex)
    #
    # @property
    # def set_latitude(self, **kwargs) -> None:
    #     """
    #     ^param kwargs: {"latitude": 00.00}
    #     :return: Here, we get kwargs and to save in db
    #     """
    #     try:
    #         self.latitude = float(kwargs.get('latitude'))
    #     except Exception as ex:
    #         raise ValueError("Check your values: %s" % ex)
    # @property
    # def get_latitude(self) -> float:
    #     """
    #     :return: this floating point number from the latitude from users db
    #     """
    #     return (lambda: float("%f") % self.latitude)()
    #
    # @property
    # def set_longitude(self, **kwargs) -> None:
    #     """
    #     ^param kwargs: {"longitude": 00.00}
    #     :return: Here, we get kwargs and to save in db
    #     """
    #     try:
    #         self.longitude = float(kwargs.get('longitude'))
    #     except Exception as ex:
    #         raise ValueError("Check your values: %s" % ex)
    #
    # @property
    # def get_longitude(self) -> float:
    #     """
    #     :return: this floating point number from the latitude from users db
    #     """
    #     return (lambda: float("%f") % self.longitude)()

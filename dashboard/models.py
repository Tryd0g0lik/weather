"""
dashboard/models.py
"""

import logging

from typing import Dict, TypeVar
from asgiref.sync import sync_to_async

from rest_framework_simplejwt.tokens import TokenUser

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from project.settings import SIMPLE_JWT
from django.utils.translation import gettext_lazy as _

# Create your models here.

from logs import configure_logging

configure_logging(logging.INFO)
log = logging.getLogger(__name__)
AuthUser = TypeVar("AuthUser", "Users", TokenUser)


class Users(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=30,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[
            MinLengthValidator(
                3, message=_("Name should be at least 3 characters")
            ),
            MaxLengthValidator(
                30, _("Name should be less than 30  or 30 characters")
            ),
            RegexValidator(
                regex=r"(^[a-zA-Z][a-zA-Z_]{2,30}$|^$)",
                message=_(
                    "Name should contain only characters\
from a-z and A-Z and digits"
                ),
            ),
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    password = models.CharField(
        _("password"),
        max_length=128,
        validators=[
            MaxLengthValidator(
                7, message=_("Maximum quantity of symbols before 7 symbols/characters")
            ),
            MinLengthValidator(
                2, message=_("Minimum quantity of symbols is 2 symbols/characters")
            ),
            RegexValidator(
                regex=r"(^[a-zA-Z%0-9}{_%]{2,30}$|^$)",
                message=_("The password's characters is valid"),
            )
        ]
        )
    latitude = models.FloatField(
        _("latitude"),
        max_length=7,
        blank=True,
        default=0.0,
        help_text=_("latitude for forecast"),
        validators=[
            MaxLengthValidator(
                7, message=_("Maximum quantity of symbols before 7 symbols/characters")
            ),
            MinLengthValidator(
                2, message=_("Minimum quantity of symbols is 2 symbols/characters")
            ),
        ],
    )
    longitude = models.FloatField(
        _("longitude"),
        max_length=7,
        blank=True,
        default=0.0,
        help_text=_("longitude for forecast"),
        validators=[
            MaxLengthValidator(
                7, message=_("Maximum quantity of symbols before 7 symbols/characters")
            ),
            MinLengthValidator(
                2, message=_("Minimum quantity of symbols is 2 symbols/characters")
            ),
        ],
    )

    def __str__(self):
        return "Latitude: %s. Latitude: %s" % (self.latitude, self.latitude)

    class Meta:
        db_table = "users"
        # fields = ["username", "latitude", "longitude", "ix_active", "last_name", ]

    def set_latitude(self, **kwargs) -> None:
        """
        ^param kwargs: {"latitude": 00.00}
        :return: Here, we get kwargs and to save in db
        """
        try:
            self.latitude = float(kwargs.get("latitude"))
            log.info("User: %s, Latitude: %s" % (self.username, self.latitude))
        except Exception as ex:
            raise ValueError("Check your values: %s" % ex)

    @property
    def get_latitude(self) -> float:
        """
        :return: this floating point number from the latitude from users db
        """
        return (lambda: float("%f") % self.latitude)()

    @property
    def set_longitude(self, **kwargs) -> None:
        """
        ^param kwargs: {"longitude": 00.00}
        :return: Here, we get kwargs and to save in db
        """
        try:
            self.longitude = float(kwargs.get("longitude"))
            log.info("User: %s, Longitude: %s" % (self.username, self.longitude))
        except Exception as ex:
            raise ValueError("Check your values: %s" % ex)

    @property
    def get_longitude(self) -> float:
        """
        :return: this floating point number from the latitude from users db
        """
        return (lambda: float("%f") % self.longitude)()

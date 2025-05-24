from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator
)
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
                mmessage=_("Maximum quantity of symbols before 7 symbols/characters")
            ),
            MinLengthValidator(
                2,
                massesge=_("Minimum quantity of symbols is 2 symbols/characters")
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
                mmessage=_("Maximum quantity of symbols before 7 symbols/characters")
            ),
            MinLengthValidator(
                2,
                massesge=_("Minimum quantity of symbols is 2 symbols/characters")
            )
        ]
    )

    
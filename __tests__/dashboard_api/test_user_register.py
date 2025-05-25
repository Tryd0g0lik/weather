"""
__tests__/dashboard/test_user_register.py
"""

import logging
import json
import pytest
from asgiref.sync import sync_to_async
from rest_framework import status
from django.core.cache import cache
from __tests__.fixtures import client, cleaner
from logs import configure_logging

configure_logging(logging.INFO)
log = logging.getLogger(__name__)


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestUsers:
    LIST_URL = ["/api/v1/users/index/", "/api/v1/users/index/0/login_user/"]
    VALID_DATA = {"password": "ds2Rssa8%sa", "username": "Victorovich"}

    @pytest.mark.users
    async def test_user_create_valid(self, client, cleaner):
        log.info("START TEST - USER CREATE VALID")
        """Arrange"""
        cache.clear()

        """Act"""
        response = await sync_to_async(client.post)(
            self.LIST_URL[0], data=self.VALID_DATA
        )
        log.info("GET RESPONSE FROM POST REQUEST %s" % str(response.status_code))
        assert response.status_code == status.HTTP_201_CREATED
        await sync_to_async(cleaner)(client)
        log.info("END TEST - USER CREATE VALID")

    @pytest.mark.parametrize(
        "password, username",
        [
            ("ds 2Rssa8%sa", "Victorovich"),
            ("ds2-Rssa8%sa", "Victorovich"),
            ("ds2Rssa8%sa", ""),
            ("", "Victorovich"),
            ("ss", "234567890"),
        ],
    )
    @pytest.mark.users
    async def test_user_create_invalid(self, client, cleaner, password, username):
        log.info("START TEST - USER CREATE INVALID")
        """Arrange"""
        cache.clear()

        """Act"""
        log.info("INVALID DATA - PASSWORD: %s, USERNAME: %s" % (password, username))
        response = await sync_to_async(client.post)(
            self.LIST_URL[0], data={"password": password, "username": username}
        )
        log.info("GET RESPONSE FROM POST REQUEST %s" % str(response.status_code))
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        await sync_to_async(cleaner)(client)
        log.info("END TEST - USER NO CREATE - OK")

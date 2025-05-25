import pytest
import logging
from asgiref.sync import sync_to_async
from rest_framework.test import APIClient
from django.db import connections

from logs import configure_logging

configure_logging(logging.INFO)
log = logging.getLogger(__name__)


@pytest.fixture(autouse=True, scope="module")
def client():
    """Created a client to the testing"""
    client = APIClient()
    log.info("CREATING CLIENT")
    return client


@pytest.fixture
def cleaner():
    """Clears all connections and clients"""

    def clear_process_all(client):
        log.info("CLEANER IS START")
        client.logout()
        log.info("CLEANER LOGOUT CLIENT")
        connections.close_all()
        log.info("CLEANER CLOSED CONNECTIONS FOR CLIENT")

    return clear_process_all

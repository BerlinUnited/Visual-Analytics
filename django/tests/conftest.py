import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .user.factories import UserFactory
from user.models import Organization


@pytest.fixture
def admin_client():
    """client with create,modify and delete permissions"""
    admin_org, created = Organization.objects.get_or_create(name="berlin_united")
    user = UserFactory.create(organization=admin_org)
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


@pytest.fixture
def auth_client():
    """client with read only permissions"""
    user = UserFactory.create()
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


@pytest.fixture
def client():
    """client with no permissions"""
    client = APIClient()
    return client

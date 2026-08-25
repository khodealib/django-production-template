import pytest
from rest_framework.test import APIClient

from src.users.factories import UserFactory


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def authenticated_client(api_client: APIClient, user) -> APIClient:
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_user(db):
    return UserFactory(is_staff=True, is_superuser=True)


@pytest.fixture
def admin_client(api_client: APIClient, admin_user) -> APIClient:
    api_client.force_authenticate(user=admin_user)
    return api_client

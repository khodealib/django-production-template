import pytest
from rest_framework.test import APIClient

from src.users.factories import UserFactory


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db):  # noqa: ANN001
    return UserFactory()


@pytest.fixture
def authenticated_client(api_client: APIClient, user) -> APIClient:  # noqa: ANN001
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_user(db):  # noqa: ANN001
    return UserFactory(is_staff=True, is_superuser=True)


@pytest.fixture
def admin_client(api_client: APIClient, admin_user) -> APIClient:  # noqa: ANN001
    api_client.force_authenticate(user=admin_user)
    return api_client

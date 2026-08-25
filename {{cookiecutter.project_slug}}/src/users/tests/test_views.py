import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.users.factories import UserFactory


@pytest.mark.django_db
class TestUserViewSet:
    def test_list_users_authenticated(self, authenticated_client: APIClient) -> None:
        UserFactory.create_batch(3)
        response = authenticated_client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK

    def test_list_users_unauthenticated(self, api_client: APIClient) -> None:
        response = api_client.get("/api/users/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_user(self, authenticated_client: APIClient, user) -> None:  # noqa: ANN001
        response = authenticated_client.get(f"/api/users/{user.pk}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email  # type: ignore[index]

    def test_create_user(self, api_client: APIClient) -> None:
        payload = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "testpass123",
        }
        response = api_client.post("/api/users/", payload)
        assert response.status_code == status.HTTP_201_CREATED

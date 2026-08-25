import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.users.factories import UserFactory


@pytest.mark.django_db
class TestUserViewSet:
    def test_list_users_enveloped(self, admin_client: APIClient) -> None:
        UserFactory.create_batch(3)
        response = admin_client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK

        payload = response.json()
        assert set(payload) == {"success", "pagination", "data", "errors"}
        assert payload["success"] is True
        assert payload["pagination"]["count"] == 3
        assert len(payload["data"]) == 3

    def test_list_users_anonymous_is_enveloped_success(
        self, api_client: APIClient
    ) -> None:
        # IsOwnerOrReadOnly replaces IsAuthenticated, so anonymous list
        # requests are permitted and see an empty queryset.
        response = api_client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK

        payload = response.json()
        assert payload["success"] is True
        assert payload["data"] == []
        assert payload["pagination"]["count"] == 0

    def test_retrieve_user(self, authenticated_client: APIClient, user) -> None:  # noqa: ANN001
        response = authenticated_client.get(f"/api/users/{user.pk}/")
        assert response.status_code == status.HTTP_200_OK

        payload = response.json()
        assert payload["success"] is True
        assert payload["pagination"] is None
        assert payload["data"]["email"] == user.email

    def test_create_user(self, api_client: APIClient) -> None:
        payload = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "testpass123",
        }
        response = api_client.post("/api/users/", payload)
        assert response.status_code == status.HTTP_201_CREATED

        body = response.json()
        assert body["success"] is True
        assert body["data"]["username"] == "newuser"

    def test_all_users_non_paginated(self, admin_client: APIClient) -> None:
        UserFactory.create_batch(25)
        response = admin_client.get("/api/users/all/")
        assert response.status_code == status.HTTP_200_OK

        body = response.json()
        assert body["pagination"] is None
        assert len(body["data"]) == 26  # batch + the authenticating admin user

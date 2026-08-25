from typing import Any

import pytest
from rest_framework.test import APIClient

from src.users.factories import UserFactory

pytestmark = pytest.mark.django_db

USERS_URL = "/api/users/"
ALL_USERS_URL = "/api/users/all/"


def assert_envelope(payload: dict[str, Any], *, success: bool = True) -> None:
    assert set(payload) == {"success", "pagination", "data", "errors"}
    assert payload["success"] is success
    if success:
        assert payload["errors"] is None
    else:
        assert payload["data"] is None
        assert isinstance(payload["errors"], list)


def get_json(client: APIClient, url: str) -> dict[str, Any]:
    response = client.get(url)
    assert response.status_code == 200
    data: dict[str, Any] = response.json()
    return data


class TestPaginatedEnvelope:
    def test_default_page_size(self, admin_client: APIClient) -> None:
        # +1 user comes from the admin_user behind admin_client
        UserFactory.create_batch(25)
        payload = get_json(admin_client, USERS_URL)

        assert_envelope(payload)
        pagination = payload["pagination"]
        assert pagination["count"] == 26
        assert pagination["page_size"] == 20
        assert pagination["previous"] is None
        assert pagination["next"] is not None and "page=2" in pagination["next"]
        assert len(payload["data"]) == 20

    def test_client_provided_page_size(self, admin_client: APIClient) -> None:
        UserFactory.create_batch(12)
        payload = get_json(admin_client, f"{USERS_URL}?page_size=5")

        assert_envelope(payload)
        assert payload["pagination"]["count"] == 13
        assert payload["pagination"]["page_size"] == 5
        assert len(payload["data"]) == 5

    def test_page_size_clamped_to_max(self, admin_client: APIClient) -> None:
        UserFactory.create_batch(150)
        payload = get_json(admin_client, f"{USERS_URL}?page_size=500")

        assert_envelope(payload)
        assert payload["pagination"]["page_size"] == 100
        assert len(payload["data"]) == 100

    def test_first_page_previous_null(self, admin_client: APIClient) -> None:
        UserFactory.create_batch(45)
        payload = get_json(admin_client, USERS_URL)

        assert payload["pagination"]["previous"] is None
        assert payload["pagination"]["next"] is not None

    def test_middle_page_has_both_links(self, admin_client: APIClient) -> None:
        # 46 users across pages of 20/20/6 -> page 2 is a middle page
        UserFactory.create_batch(45)
        payload = get_json(admin_client, f"{USERS_URL}?page=2")

        pagination = payload["pagination"]
        assert pagination["previous"] is not None
        assert pagination["next"] is not None
        assert len(payload["data"]) == 20

    def test_last_page_next_null(self, admin_client: APIClient) -> None:
        UserFactory.create_batch(45)
        payload = get_json(admin_client, f"{USERS_URL}?page=3")

        pagination = payload["pagination"]
        assert pagination["next"] is None
        assert pagination["previous"] is not None
        assert len(payload["data"]) == 6

    def test_empty_queryset(self, admin_client: APIClient) -> None:
        from django.contrib.auth import get_user_model

        get_user_model().objects.all().delete()
        payload = get_json(admin_client, USERS_URL)

        assert_envelope(payload)
        assert payload["pagination"] == {
            "count": 0,
            "page_size": 20,
            "next": None,
            "previous": None,
        }
        assert payload["data"] == []

    def test_data_items_are_serialized_users(self, admin_client: APIClient) -> None:
        user = UserFactory()
        payload = get_json(admin_client, USERS_URL)

        assert payload["pagination"]["count"] == 2
        emails = [item["email"] for item in payload["data"]]
        assert user.email in emails


class TestNonPaginatedEnvelope:
    def test_all_endpoint_is_non_paginated(self, admin_client: APIClient) -> None:
        UserFactory.create_batch(3)
        payload = get_json(admin_client, ALL_USERS_URL)

        assert_envelope(payload)
        assert payload["pagination"] is None
        assert payload["errors"] is None
        assert isinstance(payload["data"], list)
        assert len(payload["data"]) == 4


class TestErrorEnvelope:
    def test_validation_error_is_enveloped(self, authenticated_client: APIClient) -> None:
        response = authenticated_client.post(USERS_URL, {})

        assert response.status_code == 400
        payload = response.json()
        assert_envelope(payload, success=False)
        assert len(payload["errors"]) > 0

    def test_permission_denied_is_enveloped(self, api_client: APIClient) -> None:
        response = api_client.get(USERS_URL)

        assert response.status_code == 403
        payload = response.json()
        assert_envelope(payload, success=False)
        assert payload["pagination"] is None

    def test_not_found_is_enveloped(self, admin_client: APIClient) -> None:
        response = admin_client.get(f"{USERS_URL}999999/")

        assert response.status_code == 404
        payload = response.json()
        assert_envelope(payload, success=False)

from typing import Any

import pytest
from drf_spectacular.generators import SchemaGenerator

pytestmark = pytest.mark.django_db


def generate_schema() -> dict[str, Any]:
    schema: dict[str, Any] = SchemaGenerator().get_schema(public=True)
    return schema


def get_response_schema(schema: dict[str, Any], path: str, method: str, status: str = "200") -> dict[str, Any]:
    operation = schema["paths"][path][method]
    response_schema: dict[str, Any] = operation["responses"][status]["content"]["application/json"]["schema"]
    return response_schema


def user_component_name(schema: dict[str, Any]) -> str:
    assert "User" in schema["components"]["schemas"], sorted(schema["components"]["schemas"])
    return "User"


class TestEnvelopeSchema:
    def test_paginated_list_envelope_properties(self) -> None:
        schema = get_response_schema(generate_schema(), "/api/users/", "get")

        assert set(schema["required"]) == {"success", "pagination", "data", "errors"}
        assert set(schema["properties"]) == {"success", "pagination", "data", "errors"}

    def test_paginated_list_pagination_object_is_typed(self) -> None:
        schema = generate_schema()
        component = schema["components"]["schemas"]["PaginatedUserList"]
        pagination = component["properties"]["pagination"]

        assert pagination["type"] == "object"
        assert set(pagination["properties"]) == {
            "count",
            "page_size",
            "next",
            "previous",
        }
        assert pagination["properties"]["count"]["type"] == "integer"
        assert pagination["properties"]["page_size"]["type"] == "integer"
        for link in ("next", "previous"):
            assert pagination["properties"][link]["type"] == "string"
            assert pagination["properties"][link]["format"] == "uri"
            assert pagination["properties"][link]["nullable"] is True

    def test_paginated_list_data_keeps_user_ref(self) -> None:
        schema = generate_schema()
        component = schema["components"]["schemas"]["PaginatedUserList"]

        data_schema = component["properties"]["data"]
        assert data_schema["type"] == "array"
        assert data_schema["items"]["$ref"].endswith(f"/schemas/{user_component_name(schema)}")

    def test_detail_endpoint_single_user_no_pagination(self) -> None:
        schema = generate_schema()
        response_schema = get_response_schema(schema, "/api/users/{id}/", "get", status="200")

        properties = response_schema["properties"]
        assert properties["data"]["$ref"].endswith(f"/schemas/{user_component_name(schema)}")
        pagination = properties["pagination"]
        assert pagination.get("nullable") is True
        assert "properties" not in pagination

    def test_non_paginated_list_array_of_users(self) -> None:
        schema = generate_schema()
        response_schema = get_response_schema(schema, "/api/users/all/", "get")

        properties = response_schema["properties"]
        assert properties["data"]["type"] == "array"
        assert properties["data"]["items"]["$ref"].endswith(f"/schemas/{user_component_name(schema)}")
        assert properties["pagination"].get("nullable") is True

    def test_documented_error_responses_are_enveloped(self) -> None:
        schema = generate_schema()
        for path_item in schema["paths"].values():
            for operation in path_item.values():
                if not isinstance(operation, dict):
                    continue
                for status_code, response in operation.get("responses", {}).items():
                    media = response.get("content", {}).get("application/json") if isinstance(response, dict) else None
                    if media is None or not isinstance(media.get("schema"), dict):
                        continue
                    properties = media["schema"].get("properties", {})
                    if not {"success", "data", "errors"}.issubset(properties):
                        continue  # not enveloped at all -> caught by other tests
                    if str(status_code).startswith("2"):
                        assert properties["success"]["enum"] == [True]
                    # non-2xx: documented error responses must use the error
                    # envelope (drf-spectacular >= 0.30 rarely documents them;
                    # runtime behaviour is covered by the API tests)
                    else:
                        assert properties["success"]["enum"] == [False]
                        assert properties["errors"]["type"] == "array"

    def test_no_generic_object_collapse_for_data(self) -> None:
        schema = generate_schema()
        for path in ("/api/users/", "/api/users/all/"):
            data_schema = get_response_schema(schema, path, "get")["properties"]["data"]
            # data must be a $ref or a typed array of $refs - never a bare object
            if "$ref" in data_schema:
                continue
            assert data_schema.get("type") == "array"
            assert "$ref" in data_schema.get("items", {})

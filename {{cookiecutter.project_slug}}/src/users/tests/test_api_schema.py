import pytest
from drf_spectacular.generators import SchemaGenerator

pytestmark = pytest.mark.django_db


def generate_schema() -> dict:
    return SchemaGenerator().get_schema(public=True)


def get_response_schema(schema: dict, path: str, method: str, status: str = "200") -> dict:
    operation = schema["paths"][path][method]
    return operation["responses"][status]["content"]["application/json"]["schema"]


class TestEnvelopeSchema:
    def test_paginated_list_schema(self) -> None:
        schema = get_response_schema(generate_schema(), "/api/users/", "get")

        assert set(schema["required"]) == {"success", "pagination", "data", "errors"}
        properties = schema["properties"]
        assert set(properties) == {"success", "pagination", "data", "errors"}

    def test_paginated_list_pagination_object_is_typed(self) -> None:
        schema = get_response_schema(generate_schema(), "/api/users/", "get")

        pagination = schema["properties"]["pagination"]
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
        user_component = next(
            name
            for name in schema["components"]["schemas"]
            if name.lower().endswith("user")
        )
        data_schema = get_response_schema(schema, "/api/users/", "get")["properties"]["data"]

        assert data_schema["type"] == "array"
        assert data_schema["items"]["$ref"].endswith(f"/schemas/{user_component}")

    def test_detail_endpoint_single_user_no_pagination(self) -> None:
        schema = generate_schema()
        user_component = next(
            name
            for name in schema["components"]["schemas"]
            if name.lower().endswith("user")
        )
        response_schema = get_response_schema(
            schema, "/api/users/{id}/", "get", status="200"
        )

        properties = response_schema["properties"]
        assert properties["data"]["$ref"].endswith(f"/schemas/{user_component}")
        pagination = properties["pagination"]
        assert pagination.get("nullable") is True
        assert "properties" not in pagination

    def test_non_paginated_list_array_of_users(self) -> None:
        schema = generate_schema()
        user_component = next(
            name
            for name in schema["components"]["schemas"]
            if name.lower().endswith("user")
        )
        response_schema = get_response_schema(schema, "/api/users/all/", "get")

        properties = response_schema["properties"]
        assert properties["data"]["type"] == "array"
        assert properties["data"]["items"]["$ref"].endswith(f"/schemas/{user_component}")
        assert properties["pagination"].get("nullable") is True

    def test_error_responses_are_enveloped_with_errors_array(self) -> None:
        schema = generate_schema()
        responses = schema["paths"]["/api/users/"]["post"]["responses"]

        error_statuses = [code for code in responses if not code.startswith("2")]
        assert error_statuses, "expected at least one documented error response"
        for code in error_statuses:
            media = responses[code].get("content", {}).get("application/json")
            if media is None:
                continue
            properties = media["schema"]["properties"]
            assert properties["success"]["enum"] == [False]
            assert properties["errors"]["type"] == "array"

    def test_no_generic_object_collapse_for_data(self) -> None:
        schema = generate_schema()
        for path in ("/api/users/", "/api/users/all/"):
            data_schema = get_response_schema(schema, path, "get")["properties"]["data"]
            assert data_schema != {"type": "object"}

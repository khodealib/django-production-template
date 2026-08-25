from typing import Any

from drf_spectacular.openapi import AutoSchema

from src.common.pagination import PAGINATION_SCHEMA

ENVELOPE_KEYS = frozenset({"success", "data"})


class EnvelopeAutoSchema(AutoSchema):
    """AutoSchema for enveloped APIs.

    Paginated lists are enveloped by the pagination class itself
    (``get_paginated_response_schema``, consumed by drf-spectacular >= 0.30).
    Non-paginated and detail endpoints are enveloped afterwards by
    ``envelope_postprocessing_hook`` (see SPECTACULAR_SETTINGS).
    """


def _is_enveloped(schema: Any) -> bool:
    if isinstance(schema, dict):
        properties = schema.get("properties")
        if isinstance(properties, dict) and ENVELOPE_KEYS.issubset(properties):
            return True
    return False


def _wrap_envelope(schema: Any, *, paginated: bool, is_success: bool) -> dict[str, Any]:
    pagination_schema: Any = (
        PAGINATION_SCHEMA
        if paginated
        else {
            "type": "object",
            "nullable": True,
        }
    )
    data_schema: Any
    errors_schema: Any
    if is_success:
        data_schema = schema
        errors_schema = {"type": "array", "items": {}, "nullable": True}
    else:
        data_schema = {"type": "object", "nullable": True}
        errors_schema = {"type": "array", "items": schema} if schema is not None else {"type": "array", "items": {}}
    return {
        "type": "object",
        "properties": {
            "success": {"type": "boolean", "enum": [is_success]},
            "pagination": pagination_schema,
            "data": data_schema,
            "errors": errors_schema,
        },
        "required": ["success", "pagination", "data", "errors"],
    }


def envelope_postprocessing_hook(result: dict[str, Any], generator: Any, **kwargs: Any) -> dict[str, Any]:
    """Wrap every remaining response into the API envelope.

    Runs after component resolution; paginated responses are already enveloped
    by ``EnvelopeAutoSchema`` and are detected via the ``success`` property.
    """
    http_methods = {"get", "post", "put", "patch", "delete"}
    for path_item in result.get("paths", {}).values():
        for method, operation in path_item.items():
            if method not in http_methods or not isinstance(operation, dict):
                continue
            for status_code, response in operation.get("responses", {}).items():
                content = response.get("content", {})
                if not isinstance(content, dict):
                    continue
                for media in content.values():
                    schema = media.get("schema")
                    if schema is None or _is_enveloped(schema):
                        continue
                    media["schema"] = _wrap_envelope(
                        schema,
                        paginated=False,
                        is_success=str(status_code).startswith("2"),
                    )
    return result

from typing import Any

from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def flatten_errors(data: Any) -> list[Any]:
    errors: list[Any] = []
    if isinstance(data, dict):
        for field, value in data.items():
            if isinstance(value, list):
                errors.extend(value)
            else:
                errors.append(value)
    elif isinstance(data, list):
        errors.extend(data)
    elif data is not None:
        errors.append(data)
    return errors


def envelope_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """Wrap DRF error responses into the API envelope."""
    response = drf_exception_handler(exc, context)
    if response is None:
        return None
    response.data = {
        "success": False,
        "pagination": None,
        "data": None,
        "errors": flatten_errors(response.data),
    }
    return response

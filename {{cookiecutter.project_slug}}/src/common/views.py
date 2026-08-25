from typing import Any

from rest_framework import status, viewsets
from rest_framework.response import Response

ENVELOPE_KEYS = frozenset({"success", "data"})


class EnvelopeMixin:
    """Wrap non-paginated success responses into the API envelope.

    Responses already carrying the envelope keys are left untouched: paginated
    responses come pre-wrapped by the pagination class and error responses by
    the exception handler.
    """

    def finalize_response(  # noqa: ANN001
        self,
        request,
        response,
        *args,
        **kwargs,
    ):
        response = super().finalize_response(request, response, *args, **kwargs)  # type: ignore[misc]
        _apply_envelope(response)
        return response


def _apply_envelope(response: Any) -> None:
    if not isinstance(response, Response) or getattr(response, "exception", False):
        return
    data = getattr(response, "data", None)
    if isinstance(data, dict) and ENVELOPE_KEYS.issubset(data):
        return
    response.data = {
        "success": True,
        "pagination": None,
        "data": data,
        "errors": None,
    }


class EnvelopeModelViewSet(EnvelopeMixin, viewsets.ModelViewSet):
    """ModelViewSet whose every response follows the API envelope contract."""

    def destroy(self, request, *args, **kwargs):  # noqa: ANN001, ANN202
        """Delete with a 200 envelope instead of an empty 204 body."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"success": True, "pagination": None, "data": None, "errors": None},
            status=status.HTTP_200_OK,
        )

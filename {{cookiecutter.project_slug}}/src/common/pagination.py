from typing import Any

from rest_framework import pagination
from rest_framework.response import Response

PAGINATION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "count": {"type": "integer"},
        "page_size": {"type": "integer"},
        "next": {"type": "string", "format": "uri", "nullable": True},
        "previous": {"type": "string", "format": "uri", "nullable": True},
    },
    "required": ["count", "page_size", "next", "previous"],
}


class EnvelopePaginationMixin(pagination.BasePagination):
    """Pagination base that guarantees the API envelope contract.

    Subclasses must be real DRF pagination classes; paging itself is never
    reimplemented here. Metadata (count/next/previous) is extracted through
    the DRF pagination interface so any concrete class works.
    """

    effective_page_size: int | None = None

    def paginate_queryset(self, queryset: Any, request: Any, view: Any = None) -> Any:
        get_page_size = getattr(self, "get_page_size", None)
        if callable(get_page_size):
            self.effective_page_size = get_page_size(request)
        page = super().paginate_queryset(queryset, request, view)
        if page is not None and self.effective_page_size is None:
            self.effective_page_size = len(page.object_list)
        return page

    def get_pagination_data(self) -> dict[str, Any]:
        page = getattr(self, "page", None)
        page_size = self.effective_page_size
        if page_size is None and page is not None:
            page_size = len(page.object_list)
        return {
            "count": page.paginator.count if page is not None else 0,
            "page_size": page_size,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
        }

    def get_paginated_response(self, data: Any) -> Response:
        return Response(
            {
                "success": True,
                "pagination": self.get_pagination_data(),
                "data": data,
                "errors": None,
            }
        )

    def get_paginated_response_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        """OpenAPI representation used by drf-spectacular >= 0.30."""
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "enum": [True]},
                "pagination": PAGINATION_SCHEMA,
                "data": schema,
                "errors": {"type": "array", "items": {}, "nullable": True},
            },
            "required": ["success", "pagination", "data", "errors"],
        }


class EnvelopePageNumberPagination(
    EnvelopePaginationMixin,
    pagination.PageNumberPagination,
):
    page_size_query_param = "page_size"
    max_page_size = 100

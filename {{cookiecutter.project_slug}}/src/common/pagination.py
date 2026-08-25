from typing import Any

from rest_framework import pagination
from rest_framework.response import Response


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


class EnvelopePageNumberPagination(
    EnvelopePaginationMixin,
    pagination.PageNumberPagination,
):
    page_size_query_param = "page_size"
    max_page_size = 100

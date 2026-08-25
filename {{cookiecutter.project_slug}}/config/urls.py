from django.contrib import admin
from django.http import JsonResponse
from django.urls import URLPattern, URLResolver, include, path


def health_check(request) -> JsonResponse:  # noqa: ANN001
    return JsonResponse({"status": "ok"})


urlpatterns: list[URLPattern | URLResolver] = [
    path("health/", health_check),
    path("admin/", admin.site.urls),
    path("api/", include("src.users.urls", namespace="users")),
    path("api/schema/", include("drf_spectacular.urls", namespace="schema")),
]

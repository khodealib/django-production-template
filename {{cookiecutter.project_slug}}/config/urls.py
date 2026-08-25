from django.contrib import admin
from django.http import JsonResponse
from django.urls import URLPattern, URLResolver, include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def health_check(request) -> JsonResponse:
    return JsonResponse({"status": "ok"})


urlpatterns: list[URLPattern | URLResolver] = [
    path("health/", health_check),
    path("admin/", admin.site.urls),
    path("api/", include("src.users.urls", namespace="users")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from src.common.views import EnvelopeModelViewSet

from .selectors import get_all_users
from .serializers import UserSerializer

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from src.users.models import User

UserModel = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: object, obj: "User") -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(obj == request.user)


class UserViewSet(EnvelopeModelViewSet):
    """CRUD endpoints whose responses follow the API envelope contract."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self) -> "QuerySet[User]":
        if self.request.user.is_staff:
            return UserModel.objects.all()
        return UserModel.objects.filter(pk=self.request.user.pk)

    # Custom (non-CRUD) action: response shape isn't inferable, so document it.
    @extend_schema(responses={200: UserSerializer(many=True)})
    @action(detail=False, methods=["get"], pagination_class=None, url_path="all")
    def all_users(self, request: Request) -> Response:
        """Non-paginated user list (demonstrates the non-paginated envelope)."""
        serializer = self.get_serializer(get_all_users(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer: UserSerializer) -> None:
        serializer.save()

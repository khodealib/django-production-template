from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from src.common.views import EnvelopeModelViewSet

from .selectors import get_all_users
from .serializers import UserSerializer

User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):  # noqa: ANN001, ANN201
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class UserViewSet(EnvelopeModelViewSet):
    """CRUD endpoints whose responses follow the API envelope contract."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):  # noqa: ANN202
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)

    @action(detail=False, methods=["get"], pagination_class=None, url_path="all")
    def all_users(self, request):  # noqa: ANN001, ANN202
        """Non-paginated user list (demonstrates the non-paginated envelope)."""
        serializer = self.get_serializer(get_all_users(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):  # noqa: ANN001
        serializer.save()

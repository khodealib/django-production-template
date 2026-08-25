from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from .serializers import UserSerializer

User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):  # noqa: ANN001, ANN201
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):  # noqa: ANN202
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)

    def perform_create(self, serializer):  # noqa: ANN001
        serializer.save()

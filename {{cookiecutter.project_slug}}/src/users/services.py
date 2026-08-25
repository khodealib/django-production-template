from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from src.users.models import User

UserModel = get_user_model()


def get_active_users() -> "QuerySet[User]":
    """Return all active users."""
    return UserModel.objects.filter(is_active=True)


def get_user_by_email(email: str) -> "User | None":
    """Get a user by email address."""
    return UserModel.objects.filter(email=email).first()

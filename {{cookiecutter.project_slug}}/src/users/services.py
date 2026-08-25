from django.db.models import QuerySet
from django.contrib.auth import get_user_model

User = get_user_model()


def get_active_users() -> QuerySet:
    """Return all active users."""
    return User.objects.filter(is_active=True)


def get_user_by_email(email: str) -> User | None:
    """Get a user by email address."""
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

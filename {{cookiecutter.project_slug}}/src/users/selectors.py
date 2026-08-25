from django.contrib.auth import get_user_model
from django.db.models import QuerySet

User = get_user_model()


def get_all_users() -> QuerySet:
    """Return all users."""
    return User.objects.all()


def get_staff_users() -> QuerySet:
    """Return all staff users."""
    return User.objects.filter(is_staff=True)

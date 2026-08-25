import pytest
from django.contrib.auth import get_user_model

from src.users import services

User = get_user_model()


@pytest.mark.django_db
class TestUserServices:
    def test_get_active_users(self) -> None:
        active = services.get_active_users()
        assert active.exists() is False

    def test_get_active_users_with_data(self) -> None:
        from src.users.factories import UserFactory

        UserFactory(is_active=True)
        UserFactory(is_active=False)
        assert services.get_active_users().count() == 1

    def test_get_user_by_email_found(self) -> None:
        from src.users.factories import UserFactory

        user = UserFactory(email="found@example.com")
        result = services.get_user_by_email("found@example.com")
        assert result == user

    def test_get_user_by_email_not_found(self) -> None:
        result = services.get_user_by_email("missing@example.com")
        assert result is None

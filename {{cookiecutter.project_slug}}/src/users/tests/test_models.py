import pytest

from src.users.models import User
from src.users.factories import UserFactory


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self) -> None:
        user = UserFactory()
        assert user.pk is not None
        assert user.is_active is True

    def test_create_staff_user(self) -> None:
        user = UserFactory(is_staff=True)
        assert user.is_staff is True

    def test_create_superuser(self) -> None:
        user = UserFactory(is_staff=True, is_superuser=True)
        assert user.is_superuser is True

    def test_str_with_email(self) -> None:
        user = UserFactory(email="test@example.com")
        assert str(user) == "test@example.com"

    def test_str_without_email(self) -> None:
        user = UserFactory(email="")
        assert str(user) == user.username

    def test_ordering(self) -> None:
        users = UserFactory.create_batch(3)
        qs = User.objects.all()
        assert list(qs) == list(reversed(users))

import factory
from faker import Faker

from src.users.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances for both seeding and testing."""

    class Meta:
        model = User

    email = factory.LazyFunction(fake.email)
    username = factory.LazyFunction(fake.user_name)
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)
    is_active = True

    @factory.post_generation
    def password(self, create: bool, extracted: str | None, **kwargs) -> None:  # noqa: ANN001
        password = extracted or "testpass123"
        self.set_password(password)
        if create:
            self.save()


class StaffUserFactory(UserFactory):
    is_staff = True


class SuperUserFactory(UserFactory):
    is_staff = True
    is_superuser = True

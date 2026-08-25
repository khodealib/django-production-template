import factory
from faker import Faker

from src.users.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances for both seeding and testing."""

    class Meta:
        model = User
        # our password post_generation hook saves explicitly
        skip_postgeneration_save = True

    email = factory.LazyFunction(fake.email)
    # faker's name pool is small; guarantee uniqueness across large batches
    username = factory.Sequence(lambda n: f"{fake.user_name()}_{n}")
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)
    is_active = True

    @factory.post_generation
    def password(self: User, create: bool, extracted: str | None, **kwargs: object) -> None:
        password = extracted or "testpass123"
        self.set_password(password)
        if create:
            self.save()


class StaffUserFactory(UserFactory):
    is_staff = True


class SuperUserFactory(UserFactory):
    is_staff = True
    is_superuser = True

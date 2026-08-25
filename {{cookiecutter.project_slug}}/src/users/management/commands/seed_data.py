"""Seed the database with sample data."""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with sample data"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Flush the database before seeding",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of sample users to create (default: 10)",
        )

    def handle(self, *args, **options) -> None:
        if options["flush"]:
            self.stdout.write("Flushing database...")
            User.objects.all().delete()

        self._create_super_user()
        self._seed_users(options["count"])

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))

    def _create_super_user(self) -> None:
        import os

        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")

        if User.objects.filter(email=email).exists():
            self.stdout.write(f"Superuser {email} already exists, skipping.")
            return

        User.objects.create_superuser(
            email=email,
            username=email.split("@")[0],
            password=password,
            first_name="Admin",
            last_name="User",
        )
        self.stdout.write(self.style.SUCCESS(f"Created superuser: {email}"))

    def _seed_users(self, count: int) -> None:
        from src.users.factories import UserFactory

        existing_count = User.objects.count()
        self.stdout.write(f"Creating {count} sample users...")

        UserFactory.create_batch(count)

        total = User.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Created {total - existing_count} new users (total: {total})"))

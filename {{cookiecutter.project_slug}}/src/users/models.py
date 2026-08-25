from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model for {{ cookiecutter.project_name }}."""

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return self.email or self.username

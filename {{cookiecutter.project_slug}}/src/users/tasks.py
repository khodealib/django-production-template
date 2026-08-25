from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_welcome_email(user_id: int) -> None:
    """Send a welcome email to a newly created user."""
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return
    # TODO: implement email sending
    # from django.core.mail import send_mail
    # send_mail(
    #     subject="Welcome!",
    #     message=f"Hi {user.first_name or user.username}, welcome to {{ cookiecutter.project_name }}!",
    #     from_email="noreply@example.com",
    #     recipient_list=[user.email],
    # )

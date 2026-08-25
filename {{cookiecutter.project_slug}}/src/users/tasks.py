from celery import shared_task


@shared_task
def send_welcome_email(user_id: int) -> None:
    """Send a welcome email to a newly created user."""
    from django.contrib.auth import get_user_model

    if not get_user_model().objects.filter(pk=user_id).exists():
        return
    # TODO: implement email sending
    # from django.core.mail import send_mail
    # send_mail(
    #     subject="Welcome!",
    #     message=f"Hi {user.first_name or user.username}, welcome to {{ cookiecutter.project_name }}!",
    #     from_email="noreply@example.com",
    #     recipient_list=[user.email],
    # )

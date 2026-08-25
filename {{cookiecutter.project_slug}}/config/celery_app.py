from celery import Celery

app = Celery("{{ cookiecutter.project_slug }}")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self: Celery) -> None:
    print(f"Request: {self.request!r}")

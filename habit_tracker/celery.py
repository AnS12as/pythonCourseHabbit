from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habit_tracker.settings")

app = Celery("habit_tracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

import os
from django.apps import apps
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habit_tracker.settings")

app = Celery("habit_tracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.autodiscover_tasks(lambda: [app_config.name for app_config in apps.get_app_configs()])

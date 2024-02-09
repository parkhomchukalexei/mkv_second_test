import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mkv_second_test.settings")

app = Celery("mkv_second_test")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
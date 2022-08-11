from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adesua.settings")

app = Celery("adesua")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print(f"Request: {self.request!r}")

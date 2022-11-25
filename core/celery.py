import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'core.settings')

app = Celery('core')
app.config_from_object('django.conf.settings', namespace="CELERY")
app.autodiscover_tasks()

# celery beat schedule
app.conf.beat_schedule = {
    "scheduled_task": {
        "task": "wallet.tasks.form_statistics",
        "schedule": crontab(minute=0, hour=12),
    }
}
# routing
app.conf.task_routes = {
    "wallet.tasks.send_notification": "mailing_queue",
    "wallet.tasks.form_statistics": "stats_queue",
}

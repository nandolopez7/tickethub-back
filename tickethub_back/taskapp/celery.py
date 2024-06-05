"""Celery app config."""

import os
from celery import Celery
from django.apps import apps, AppConfig
from django.conf import settings

from celery.schedules import crontab

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  


app = Celery('tickethub_back')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'ejecucion-automatica-web-scraping-periodic': {
        'task': 'ejecucion_automatica_web_scraping',
        'schedule': crontab(hour='14', minute='58')
    }
}
print('***** app.conf.beat_schedule: ', app.conf.beat_schedule)
app.conf.timezone = 'America/Bogota'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

class CeleryAppConfig(AppConfig):
    name = 'tickethub_back.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

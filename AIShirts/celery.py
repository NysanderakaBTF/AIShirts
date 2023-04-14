import os
from datetime import timedelta

from celery import Celery, shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AIShirts.settings')

app = Celery('AIShirts')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'reset_limit': {
        'task': 'cust_and_stuff.tasks.reset_generation_count',
        'schedule': timedelta(seconds=10),
    },
    'clean_prompts': {
        'task': 'aiintegration.tasks.delete_unused_prompts',
        'schedule': timedelta(seconds=10)
    },
    'clean_images': {
        'task': 'aiintegration.tasks.clean_unused_images',
        'schedule': timedelta(seconds=10)
    },
}

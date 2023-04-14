from celery import shared_task
from django.utils import timezone

from AIShirts.celery import app
from .models import Customer

@app.task
def reset_generation_count():
    time_24_hours_ago = timezone.now() - timezone.timedelta(hours=24)
    customers = Customer.objects.filter(last_count__lte=time_24_hours_ago)
    num = 0
    print('!!!!!!!!')
    for customer in customers:
        num += 1
        customer.generation_count = 0
        customer.save()
    return 'Users reseted: '+str(num)


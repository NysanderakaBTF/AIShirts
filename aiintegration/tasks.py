import os
from datetime import timezone
from os import listdir
from os.path import join, isfile

from celery import shared_task

from AIShirts.celery import app
from aiintegration.models import Prompt, Image
from shop.models import OrderItem


@app.task
def delete_unused_prompts():
    print("!!!!!")
    ordered_items = OrderItem.objects.all().only("pk")
    time_2_month_ago = timezone.now() - timezone.timedelta(days=7)
    prompts_to_delete = Prompt.objects.filter(updated_at__lte=time_2_month_ago).exclude(pk__in=ordered_items)
    prompts_to_delete.delete()


@app.task
def clean_unused_images():
    print("!!!!!")
    path = os.path.dirname('../media/images')
    images = [i for i in listdir(path) if isfile(join(path, i))]
    existing_images = list(Image.objects.all().only('image_path'))
    images_to_delete = images.filter(lambda x: x not in existing_images)
    for i in images_to_delete:
        os.remove(images_to_delete)

    return images, existing_images, images_to_delete





import os
import random

from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from cust_and_stuff.models import Customer


class Image(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, verbose_name='image', null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    is_final = models.BooleanField(default=False, blank=True)
    prompt = models.ForeignKey('Prompt', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.description

    # def image_tag(self):
    #     return mark_safe('<img src="/images/%s" width="150" height="150" />' % self.image)
    #
    # image_tag.short_description = 'Image'

    @property
    def filename(self):
        return os.path.basename(self.image.name)


class ModelSceduler(models.Model):
    name = models.CharField(max_length=50)


class AiModel(models.Model):
    name = models.CharField(max_length=50)
    access_url = models.CharField(max_length=2048)
    description = models.TextField(blank=True)
    parameters = ArrayField(ArrayField(models.CharField(max_length=255), size=2), blank=True)


class Prompt(models.Model):
    prompt = models.TextField(blank=True)
    negative_prompt = models.TextField(blank=True)
    width = models.SmallIntegerField(default=768, validators=[MinValueValidator(128), MaxValueValidator(1024)])
    height = models.SmallIntegerField(default=768, validators=[MinValueValidator(128), MaxValueValidator(1024)])
    prompt_strenght = models.FloatField(default=0.8, validators=[MinValueValidator(0), MaxValueValidator(1)])
    num_outputs = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])
    num_steps = models.SmallIntegerField(default=50, validators=[MinValueValidator(1), MaxValueValidator(500)])
    guidance_scale = models.FloatField(default=7.5, validators=[MinValueValidator(1), MaxValueValidator(20)])
    scheduler = models.ForeignKey(ModelSceduler, on_delete=models.SET_NULL, null=True, blank=True)

    ai_model = models.ForeignKey(AiModel, on_delete=models.SET_NULL, null=True, blank=True)

    seed = models.IntegerField(default=random.randint(0, 1000000000000))
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)

    is_template = models.BooleanField(default=False)
    is_final = models.BooleanField(default=False)

    def __str__(self):
        return self.prompt

# Generated by Django 4.1.7 on 2023-03-31 07:11

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AiModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('access_url', models.CharField(max_length=2048)),
                ('description', models.TextField(blank=True)),
                ('parameters', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=2), blank=True, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='image')),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_final', models.BooleanField(blank=True, default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ModelSceduler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.TextField(blank=True)),
                ('negative_prompt', models.TextField(blank=True)),
                ('width', models.SmallIntegerField(default=768, validators=[django.core.validators.MinValueValidator(128), django.core.validators.MaxValueValidator(1024)])),
                ('height', models.SmallIntegerField(default=768, validators=[django.core.validators.MinValueValidator(128), django.core.validators.MaxValueValidator(1024)])),
                ('prompt_strenght', models.FloatField(default=0.8, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('num_outputs', models.SmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('num_steps', models.SmallIntegerField(default=50, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(500)])),
                ('guidance_scale', models.FloatField(default=7.5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)])),
                ('seed', models.IntegerField(default=752186096456)),
                ('is_template', models.BooleanField(default=False)),
                ('is_final', models.BooleanField(default=False)),
                ('ai_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aiintegration.aimodel')),
            ],
        ),
    ]

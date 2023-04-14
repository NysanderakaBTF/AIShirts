# Generated by Django 4.1.7 on 2023-04-12 12:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aiintegration', '0013_alter_prompt_seed'),
    ]

    operations = [
        migrations.AddField(
            model_name='prompt',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prompt',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='prompt',
            name='seed',
            field=models.IntegerField(blank=True, default=290314),
        ),
    ]

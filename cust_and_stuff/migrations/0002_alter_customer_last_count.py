# Generated by Django 4.1.7 on 2023-03-31 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cust_and_stuff', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='last_count',
            field=models.DateTimeField(null=True),
        ),
    ]

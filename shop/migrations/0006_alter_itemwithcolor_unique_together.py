# Generated by Django 4.1.7 on 2023-04-05 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_remove_itemwithcolor_size_itemwithcolor_size'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='itemwithcolor',
            unique_together={('item', 'color', 'item_code')},
        ),
    ]

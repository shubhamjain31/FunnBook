# Generated by Django 3.1.2 on 2020-10-14 13:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserPage', '0002_auto_20201014_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]

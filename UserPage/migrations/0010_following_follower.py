# Generated by Django 3.1.2 on 2020-10-15 16:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserPage', '0009_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='following',
            name='follower',
            field=models.ManyToManyField(related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]

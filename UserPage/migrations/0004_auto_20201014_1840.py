# Generated by Django 3.1.2 on 2020-10-14 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserPage', '0003_auto_20201014_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
# Generated by Django 4.2.4 on 2023-11-16 09:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlazeApp', '0013_rename_date_notification_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='liked_post', to=settings.AUTH_USER_MODEL),
        ),
    ]

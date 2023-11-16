# Generated by Django 4.2.4 on 2023-11-16 09:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlazeApp', '0014_alter_post_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='share',
            old_name='date',
            new_name='timestamp',
        ),
        migrations.AlterField(
            model_name='event',
            name='likes',
            field=models.ManyToManyField(related_name='liked_events', to=settings.AUTH_USER_MODEL),
        ),
    ]

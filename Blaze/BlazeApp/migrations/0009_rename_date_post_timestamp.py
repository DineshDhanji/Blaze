# Generated by Django 4.2.4 on 2023-11-16 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlazeApp', '0008_alter_notification_options_alter_reply_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='date',
            new_name='timestamp',
        ),
    ]

# Generated by Django 4.2.4 on 2023-11-16 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlazeApp', '0019_rename_timestamp_comment_timestam'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='timestam',
            new_name='timestamp',
        ),
    ]

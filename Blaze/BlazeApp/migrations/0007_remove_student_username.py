# Generated by Django 4.2.4 on 2023-10-16 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlazeApp', '0006_remove_user_is_student_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='username',
        ),
    ]

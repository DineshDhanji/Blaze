# Generated by Django 4.2.4 on 2023-11-15 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlazeApp', '0005_reply_user_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.AddField(
            model_name='comment',
            name='category',
            field=models.CharField(choices=[('Post', 'Post'), ('Event', 'Event')], default='Post', max_length=10),
        ),
        migrations.AddField(
            model_name='comment',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
# Generated by Django 4.2.4 on 2023-11-15 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlazeApp', '0002_post_likes_question_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='category',
        ),
    ]
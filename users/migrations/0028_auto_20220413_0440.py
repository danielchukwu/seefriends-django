# Generated by Django 3.2.8 on 2022-04-13 03:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0027_auto_20220413_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='comments_privacy_except',
            field=models.ManyToManyField(blank=True, null=True, related_name='comment_privacy_except', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='settings',
            name='stories_privacy_except',
            field=models.ManyToManyField(blank=True, null=True, related_name='story_privacy_except', to=settings.AUTH_USER_MODEL),
        ),
    ]

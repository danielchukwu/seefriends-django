# Generated by Django 3.2.8 on 2022-03-26 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0020_alter_feed_owner'),
        ('users', '0007_profile_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='seen_post',
            field=models.ManyToManyField(blank=True, to='homeapp.Post'),
        ),
        migrations.AddField(
            model_name='profile',
            name='seen_tell',
            field=models.ManyToManyField(blank=True, to='homeapp.Tell'),
        ),
    ]
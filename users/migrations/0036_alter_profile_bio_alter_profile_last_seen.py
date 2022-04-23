# Generated by Django 4.0.4 on 2022-04-19 13:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0035_alter_profile_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_seen',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 19, 14, 8, 36, 264474), null=True),
        ),
    ]
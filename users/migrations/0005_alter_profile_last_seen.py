# Generated by Django 4.0.4 on 2022-06-20 07:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_seen',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 20, 8, 11, 27, 737834), null=True),
        ),
    ]
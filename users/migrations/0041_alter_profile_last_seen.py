# Generated by Django 4.0.4 on 2022-06-04 10:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0040_alter_profile_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_seen',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 4, 11, 14, 16, 512495), null=True),
        ),
    ]
# Generated by Django 4.0.4 on 2022-06-19 18:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0051_alter_profile_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_seen',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 19, 19, 54, 45, 406322), null=True),
        ),
    ]

# Generated by Django 4.0.4 on 2022-06-19 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0054_rename_profile_uprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uprofile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

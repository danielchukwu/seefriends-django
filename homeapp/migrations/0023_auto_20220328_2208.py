# Generated by Django 3.2.8 on 2022-03-28 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0022_savepost_savetell'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savetell',
            name='tell',
        ),
        migrations.RemoveField(
            model_name='savetell',
            name='user',
        ),
        migrations.DeleteModel(
            name='SavePost',
        ),
        migrations.DeleteModel(
            name='SaveTell',
        ),
    ]
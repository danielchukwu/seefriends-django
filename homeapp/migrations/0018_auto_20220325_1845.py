# Generated by Django 3.2.8 on 2022-03-25 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0017_auto_20220325_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='tell',
            name='body',
            field=models.TextField(),
        ),
    ]

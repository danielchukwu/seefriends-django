# Generated by Django 3.2.8 on 2022-03-26 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.ImageField(default='icons/user.png', upload_to='profiles/'),
        ),
    ]

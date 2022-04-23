# Generated by Django 3.2.8 on 2022-03-30 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0021_delete_userfollower'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFollower',
            fields=[
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('follower_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by_user', to=settings.AUTH_USER_MODEL)),
                ('me', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
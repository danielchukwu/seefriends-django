# Generated by Django 4.0.4 on 2022-06-19 20:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homeapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('last_seen', models.BooleanField(default=True)),
                ('stories_privacy', models.CharField(default='Everyone', max_length=20, null=True)),
                ('read_reciet', models.BooleanField(default=True)),
                ('top_all', models.BooleanField(default=False)),
                ('top_unread', models.BooleanField(default=True)),
                ('dark_mode_chat', models.BooleanField(default=False)),
                ('private_account', models.BooleanField(default=False)),
                ('comments_privacy', models.CharField(default='Everyone', max_length=20, null=True)),
                ('dark_mode_account', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('comments_privacy_except', models.ManyToManyField(blank=True, related_name='comment_privacy_except', to=settings.AUTH_USER_MODEL)),
                ('owner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('stories_privacy_except', models.ManyToManyField(blank=True, related_name='story_privacy_except', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Settings',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('username', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=500, null=True, unique=True)),
                ('img', models.ImageField(default='icons/user.png', upload_to='profiles/')),
                ('bio', models.TextField(blank=True, default='', null=True)),
                ('online', models.BooleanField(default=False)),
                ('last_seen', models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 19, 21, 52, 19, 819438), null=True)),
                ('verified', models.BooleanField(default=False)),
                ('activity_count', models.PositiveSmallIntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('followers', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('friends', models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL)),
                ('saved_post', models.ManyToManyField(blank=True, related_name='saved_post', to='homeapp.post')),
                ('saved_tell', models.ManyToManyField(blank=True, related_name='saved_tell', to='homeapp.tell')),
                ('seen_post', models.ManyToManyField(blank=True, to='homeapp.post')),
                ('seen_tell', models.ManyToManyField(blank=True, to='homeapp.tell')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFollowing',
            fields=[
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_a_user', to=settings.AUTH_USER_MODEL)),
                ('me', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'unique_together': {('me', 'following')},
            },
        ),
        migrations.CreateModel(
            name='UserFollower',
            fields=[
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('follower_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by_user', to=settings.AUTH_USER_MODEL)),
                ('me', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'unique_together': {('me', 'follower_to')},
            },
        ),
    ]

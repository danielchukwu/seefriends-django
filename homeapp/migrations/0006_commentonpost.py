# Generated by Django 3.2.8 on 2022-03-23 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homeapp', '0005_auto_20220323_1736'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentOnPost',
            fields=[
                ('comment', models.CharField(max_length=200)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeapp.post')),
            ],
            options={
                'ordering': ['-created', '-updated'],
            },
        ),
    ]
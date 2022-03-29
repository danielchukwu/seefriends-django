# Generated by Django 3.2.8 on 2022-03-25 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homeapp', '0014_auto_20220325_1153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ManyToManyField(blank='True', null=True, to='homeapp.Post')),
                ('tell', models.ManyToManyField(blank='True', null=True, to='homeapp.Tell')),
            ],
            options={
                'ordering': ['-created', '-updated'],
            },
        ),
    ]
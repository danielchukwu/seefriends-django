from django.contrib import admin
from .models import Profile, Settings, UserFollower, UserFollowing

# Register your models here.

admin.site.register(Profile)
admin.site.register(Settings)
admin.site.register(UserFollower)
admin.site.register(UserFollowing)
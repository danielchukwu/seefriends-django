from django.contrib import admin
from .models import UProfile, Settings, UserFollower, UserFollowing

# Register your models here.

admin.site.register(UProfile)
admin.site.register(Settings)
admin.site.register(UserFollower)
admin.site.register(UserFollowing)
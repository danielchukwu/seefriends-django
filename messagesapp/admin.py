from django.contrib import admin
from .models import Body, Message, Room

# Register your models here.

admin.site.register(Message)
admin.site.register(Body)
admin.site.register(Room)
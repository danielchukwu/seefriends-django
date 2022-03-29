from django.contrib import admin
from homeapp.models import CommentOnPost, Post, Tell, CommentOnTell, SavePost, SaveTell

# Register your models here.

admin.site.register(Post)
admin.site.register(CommentOnPost)

admin.site.register(Tell)
admin.site.register(CommentOnTell)

admin.site.register(SavePost)
admin.site.register(SaveTell)
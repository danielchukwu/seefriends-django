from django.contrib import admin
from homeapp.models import Post, PostFeed, CommentOnPost, Search, Tell, CommentOnTell, Activity, SavePost, SaveTell

# Register your models here.

admin.site.register(Post)
admin.site.register(PostFeed)
admin.site.register(CommentOnPost)

admin.site.register(Tell)
admin.site.register(CommentOnTell)

admin.site.register(SavePost)
admin.site.register(SaveTell)

admin.site.register(Activity)

admin.site.register(Search)
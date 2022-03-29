import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from users.models import *


# 1. POST
# post
class Post(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   img = models.ImageField(upload_to='contents/', null=True, blank=True)
   body = models.TextField()
   likers = models.ManyToManyField(User, 'post_likers', blank=True)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

   class Meta:
      ordering = ['-created']

   @property
   def get_total_likes(self):
      return self.likers.count()

   def __str__(self):
      return str(self.owner) + " post - " + str(self.body[:30])

# post comment
class CommentOnPost(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   post = models.ForeignKey(Post, on_delete=models.CASCADE)
   comment = models.CharField(max_length=2000)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
   
   class Meta:
      ordering = ['-created', '-updated']

   def __str__(self):
      return str(self.owner) + " commented - " + str(self.comment)


# 2. TELL
# tell
class Tell(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   body = models.TextField()
   likers = models.ManyToManyField(User, 'likers', blank=True)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

   class Meta:
      ordering = ['-created', '-updated']

   @property
   def get_total_likes(self):
      return self.likers.count()

   def __str__(self) -> str:
      return f"{str(self.owner)} tell - {str(self.body)}"

# tell comment
class CommentOnTell(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   tell = models.ForeignKey(Tell, on_delete=models.CASCADE)
   comment = models.CharField(max_length=200)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
   
   class Meta:
      ordering = ['-created', '-updated']

   def __str__(self):
      return str(self.owner) + " commented - " + str(self.comment)



# SECTION 2: SAVE POST & TELL
class SavePost(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
   
   updated = models.DateTimeField(auto_now_add=True)
   created = models.DateTimeField(auto_now=True)
   id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

   # class Meta:
   #    unique_together = ['owner', 'post']

   def __str__(self):
      return str(self.post)

class SaveTell(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   tell = models.ForeignKey(Tell, on_delete=models.CASCADE, null=True)
   
   updated = models.DateTimeField(auto_now_add=True)
   created = models.DateTimeField(auto_now=True)
   id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

   # class Meta:
   #    unique_together = ['owner', 'post']

   def __str__(self):
      return str(self.tell)
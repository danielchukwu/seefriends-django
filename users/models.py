import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import homeapp


class Profile(models.Model):
   VOTE_TYPE = (
      ('MALE', 'a male'),
      ('FEMALE', 'a female'),
   )
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   name = models.CharField(max_length=200, blank=True, null=True)
   username = models.CharField(max_length=200, blank=True, null=True)
   email = models.EmailField(max_length=500, blank=True, null=True, unique=True)
   img = models.ImageField(upload_to="profiles/", default="icons/user.png")
   gender = models.CharField(max_length=200, choices=VOTE_TYPE)
   bio = models.TextField()

   followers = models.ManyToManyField(User, related_name='followers', blank=True)
   following = models.ManyToManyField(User, related_name='following', blank=True)
   friends = models.ManyToManyField(User, related_name='friends', blank=True)
   verified = models.BooleanField(default=False)

   saved_post = models.ManyToManyField("homeapp.Post", related_name="saved_post", blank=True)
   saved_tell = models.ManyToManyField("homeapp.Tell", related_name="saved_tell", blank=True)
   
   seen_post = models.ManyToManyField("homeapp.Post", blank=True)
   seen_tell = models.ManyToManyField("homeapp.Tell", blank=True)

   updated = models.DateTimeField(auto_now_add=True)
   created = models.DateTimeField(auto_now=True)
   id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

   def __str__(self):
      return self.username
   
   @property
   def get_total_followers(self):
      return self.followers.count()
   
   @property
   def get_total_following(self):
      return self.following.count()

   @property
   def get_total_friends(self):
      return self.friends.count()


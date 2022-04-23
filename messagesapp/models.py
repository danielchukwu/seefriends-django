from datetime import datetime
from email.policy import default
from pickle import TRUE
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.

class Message(models.Model):
   owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
   recipient = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="messages", null=True, blank=True)

   request_accepted = models.BooleanField(default=False)

   unread_messages = models.IntegerField(default=0) # message: msg.2
   last_body = models.ForeignKey("Body", on_delete=models.SET_NULL, null=True, blank=True, related_name="last_body", default="") # message: msg.3
   subdate = models.DateTimeField(null=True, blank=True)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

   def __str__(self) -> str:
      return f"{self.owner} to -> {self.recipient}"

   class Meta:
      ordering = ['-updated']            # logic: so it appears in chats in the order of most recently updated
      unique_together = ['owner', 'recipient']



class Body(models.Model):
   owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
   recipient = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="body_recipient", null=True, blank=True)

   message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
   body = models.TextField()
   is_read = models.BooleanField(default=False)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

   def __str__(self) -> str:
      return f"Body -> {self.body[:50]}"

   @property
   def get_body_count(self):
      return len(self.body)

   @property
   def get_time(self):
      "we add + 1 to hour because django created time hour has a -1 bug or error. so to fix when displaying time to a user is we add 1 to the hour"
      hour = None
      minutes = None
      if self.created.hour + 1 < 10:
         hour = f"0{self.created.hour + 1}"
      else:
         hour = f"{self.created.hour + 1}"

      if self.created.minute < 10:
         minutes = f"0{self.created.minute}"
      else:
         minutes = f"{self.created.minute}"

      return f"{hour}:{minutes}"


   class Meta:
      verbose_name_plural = "Body"
      ordering = ['-created']

# purpose: for chatting in real-time
class Room(models.Model):
   room_name = models.CharField(max_length=50)
   participants = models.ManyToManyField(User, blank=True)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

   def __str__(self) -> str:
      return f"{self.room_name} room"

   @property
   def get_user_count(self):
      return self.participants.count()

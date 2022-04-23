from datetime import datetime
import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync



class OnlineConsumer(WebsocketConsumer):
   def connect(self):
      self.me = self.scope['user']
      self.status_name = "online-users"
      print("WAS HERE: OnlineConsumer")

      self.accept()
      self.send(text_data=json.dumps({
         'Online': True
      }))
      async_to_sync(self.channel_layer.group_add)(
         self.status_name,
         self.channel_name
      )
      self.me.profile.online = True
      self.me.profile.save()
   
   def disconnect(self, code):
      async_to_sync(self.channel_layer.group_discard)(
         self.status_name,
         self.channel_name
      )
      self.me.profile.online = False
      self.me.profile.last_seen = datetime.now()
      self.me.profile.save()
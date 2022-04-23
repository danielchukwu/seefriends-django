import json
from channels.generic.websocket import WebsocketConsumer
# from channels.
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from messagesapp.models import Room
from channels.db import database_sync_to_async

from .utils import *

# @database_sync_to_async
def message_creation(me, other, message, room):
   user = other
   other_message, other_created = Message.objects.get_or_create(owner=other, recipient = me)
   my_message, my_created = Message.objects.get_or_create(owner = me, recipient = other)

   # logic: reject empty messages
   reject = rejectEmptyMessageUtil(message)
   if reject != True:
      # logic: send request to user-> if friends = requests for both users true. else only one is made true
      sendRequest(user, me, other_message, my_message)
      
      body = Body.objects.create(owner=me, recipient=other_message.owner, message=my_message, body=message)
      if room.get_user_count != 2:
         my_message.unread_messages += 1     # logic -> msg.3: increment unread message on my_message to -> recipient
         my_message.save()
      else:
         messegeSeenUtil(my_message)

      # logic -> msg.3: update both user message objects to the most recent created body in chat -> purpose: all just to display in chats the most recent text and time sent 😪
      my_message.last_body = body
      other_message.last_body = body
      my_message.save()
      updateSubDate(my_message)
      other_message.save()
      updateSubDate(other_message)

def add_user_to_room(me, room_name):
   room, created = Room.objects.get_or_create(room_name = room_name)
   room.participants.add(me)
   room.save()

def remove_user_from_room(me, room_name):
   room, created = Room.objects.get_or_create(room_name = room_name)
   room.participants.remove(me)
   room.save()

class ChatConsumer(WebsocketConsumer):
   def connect(self):
      self.me = self.scope['user']
      id = self.scope['url_route']['kwargs']['pk']
      self.other = User.objects.get(id=id)   # print(f'me: {self.me} | other: {self.other}')

      if self.me.id > self.other.id:
         self.room_name = f'{self.me.id}-{self.other.id}'
      else:
         self.room_name = f'{self.other.id}-{self.me.id}'

      self.room, self.created = Room.objects.get_or_create(room_name = self.room_name)

      async_to_sync(self.channel_layer.group_add)(
         self.room_name,
         self.channel_name
      )
      # print(f'Connected Users: {room.paticipants.all}')

      self.accept()
      add_user_to_room(self.me, self.room_name)
      self.send(text_data=json.dumps({'Type': 'SEEFRIENDS LIVE', 'Room': f'{self.room_name}', 'seen': True, 'other_id': id}))
   
   
   def receive(self, text_data):
      data = json.loads(text_data)
      message = data['message']
      message_creation(self.me, self.other, message, self.room)
      if self.other in self.room.participants.all():
         seen = True
      else: seen = False
      print(f"Seen: {seen}")

      async_to_sync(self.channel_layer.group_send)(
         self.room_name,
         {
            'type': 'send_message',
            'message': message,
            'seen': seen,
         }
      )
   
   def disconnect(self, code):
      async_to_sync(self.channel_layer.group_discard)(
         self.room_name,
         self.channel_name
      )
      remove_user_from_room(self.me, self.room_name)

   def send_message(self, event):
      message = event['message']
      seen = event['seen']
      self.send(text_data=json.dumps({'type': 'chat', 'message': message, 'seen': seen}))

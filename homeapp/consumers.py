import json
from channels.generic.websocket import WebsocketConsumer

# create your consumers here

from .models import Post, Tell


class LikePostConsumer(WebsocketConsumer):
   def connect(self):
      self.user = self.scope['user']
      id = self.scope['url_route']['kwargs']['pk']  # print(f'id:{id}')
      self.post = Post.objects.get(id=id)  # print(f"post: {self.post}")
      
      self.accept() # self.send(text_data=json.dumps({'type': 'likepostConsumer live'}))

   def receive(self, text_data):
      data = json.loads(text_data)
      status = data['type']
      if status == 'like':
         print('in like')
         if self.user not in self.post.likers.all():
            self.post.likers.add(self.user)
            self.post.save()
            print('liked!.......')
      else:
         print('in dislike')
         if self.user in self.post.likers.all():
            self.post.likers.remove(self.user)
            self.post.save()
            print('unliked!........')


class LikeTellConsumer(WebsocketConsumer):
   def connect(self):
      self.user = self.scope['user']
      id = self.scope['url_route']['kwargs']['pk']  # print(f'id:{id}')
      self.tell = Tell.objects.get(id=id)  
      print(f"tell: {self.tell}")
      
      self.accept() # self.send(text_data=json.dumps({'type': 'liketellConsumer live'}))

   def receive(self, text_data):
      data = json.loads(text_data)
      status = data['type']
      if status == 'like':
         print('in like')
         if self.user not in self.tell.likers.all():
            self.tell.likers.add(self.user)
            self.tell.save()
            print('liked!.......')
      else:
         print('in dislike')
         if self.user in self.tell.likers.all():
            self.tell.likers.remove(self.user)
            self.tell.save()
            print('unliked!........')
from homeapp.models import Activity, CommentOnPost, CommentOnTell, Post, Tell
from messagesapp.models import Body, Message
from messagesapp.utils import returnChatsCountApi
from rest_framework import serializers
from users.models import Profile
from django.contrib.auth.models import User
from homeapp.api.serializers import *

# create your message serializers over here

class PostSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)

   class Meta:
      model = Post
      fields = '__all__'

class TellSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)
   class Meta:
      model = Tell
      fields = '__all__'

class BodySerializer(serializers.ModelSerializer):
   time = serializers.SerializerMethodField()

   msg_on_post = PostSerializer(many=False)
   msg_on_tell = TellSerializer(many=False)

   class Meta:
      model = Body
      fields = '__all__'

   def get_time(self, obj):
      return obj.get_time

class MessageSerializer(serializers.ModelSerializer):
   owner = UserSerializer()
   time = serializers.SerializerMethodField()
   last_body = BodySerializer(many=False)

   class Meta:
      model = Message
      fields = '__all__'

   def get_time(self, obj):
      return obj.get_time
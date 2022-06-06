from homeapp.models import Activity, CommentOnPost, CommentOnTell, Post, Tell
from messagesapp.models import Message
from messagesapp.utils import returnChatsCountApi
from rest_framework import serializers
from users.models import Profile
from django.contrib.auth.models import User


# create your message serializers over here


class MessageSerializer(serializers.ModelSerializer):
   class Meta:
      model = Message
      fields = '__all__'
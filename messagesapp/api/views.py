from multiprocessing import context
from messagesapp.api.serializers import MessageSerializer
from messagesapp.utils import returnMessages, returnMessagesCount, returnRequestsCount
from users.models import UserFollower, UserFollowing
from homeapp.models import Activity, Post, PostFeed, Tell, SavePost, SaveTell

from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.api import serializers

# create your message views here


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def messages(request):
   messages = returnMessages(request)
   print("Messages............")
   print(messages)

   messages_count = returnMessagesCount(request)     # logic: gets chats count
   requests_count = returnRequestsCount(request)   # logic: gets requests count

   serializer = MessageSerializer(messages, many=True)

   return Response(serializer.data)
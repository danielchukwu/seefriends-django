from multiprocessing import context
from messagesapp.api.serializers import BodySerializer, MessageSerializer
from messagesapp.models import Body, Message
from messagesapp.utils import acceptRequestUtil, checkSettings, messegeSeenUtil, rejectEmptyMessageUtil, returnBody, returnMessages, returnMessagesCount, returnRequestsCount, sendRequest, updateSubDate
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
   # print("Messages............")
   # print(messages)

   messages_count = returnMessagesCount(request)     # logic: gets chats count
   requests_count = returnRequestsCount(request)   # logic: gets requests count

   serializer = MessageSerializer(messages, many=True)

   return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def messageChat(request, pk):
   
   user = User.objects.get(id=pk)
   other_message, other_created = Message.objects.get_or_create(owner=user, recipient = request.user)
   my_message, my_created = Message.objects.get_or_create(owner = request.user, recipient = other_message.owner)

   update_chats_if_settings_says_top_all = checkSettings(request.user, other_message)
   
   if (request.method == "GET"):
      # logic: adding the body texts of both users together and filtering them to give a chat fill
      bodys = returnBody(user, request)

      # logic: on message open. make all messages of recipient is_read = True
      messegeSeenUtil(other_message)

      serializer = BodySerializer(bodys, many=True)
      return Response(serializer.data)

   if request.method == "POST":
      # logic: reject empty messages
      reject = rejectEmptyMessageUtil(request.data['body'])
      if reject: return Response([{"details": "can't send an empty body"}])

      # logic: send request to user-> if friends = requests for both users true. else only one is made true
      sendRequest(user, request.user, other_message, my_message)
      
      body = Body.objects.create(owner=request.user, recipient=other_message.owner, message=my_message, body=request.data['body'])
      my_message.unread_messages += 1     # logic -> msg.3: increment unread message on my_message to -> recipient
      my_message.save()

      # logic -> msg.3: update both user message objects to the most recent created body in chat -> purpose: all just to display in chats the most recent text and time sent 😪
      my_message.last_body = body
      other_message.last_body = body
      my_message.save()
      updateSubDate(my_message)
      other_message.save()
      updateSubDate(other_message)

      return Response({"details": "successful"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def requests(request):
   print("1.................")
   messages = request.user.messages.filter(request_accepted = False)
   print("2.................")
   serializer = MessageSerializer(messages, many=True)
   print("3.................")
   return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def requestsChat(request, pk):
   user = User.objects.get(id=pk)
   bodys = returnBody(user, request)
   # logic: mark messages as seen
   other_message, other_created = Message.objects.get_or_create(owner=user, recipient = request.user)
   my_message, my_created = Message.objects.get_or_create(owner = request.user, recipient = other_message.owner)
   messegeSeenUtil(other_message)
   # if other_message.request_accepted == True and my_message.request_accepted == True:
   #    return redirect(message, pk)
   return Response([])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def acceptRequest(request, pk):
   user = User.objects.get(id=pk)
   other_message, other_created = Message.objects.get_or_create(owner=user, recipient = request.user)
   my_message, my_created = Message.objects.get_or_create(owner = request.user, recipient = other_message.owner)
   acceptRequestUtil(other_message, my_message)

   return Response({"details: successful!"})

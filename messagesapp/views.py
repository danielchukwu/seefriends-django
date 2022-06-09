from django.shortcuts import render, redirect
from .models import Body, Message, Room
from django.contrib.auth.models import User

from django.db.models import Q

from .utils import *
# Create your views here.

def chat(request):
   chats = returnMessages(request)

   chats_count = returnMessagesCount(request)     # logic: gets chats count
   requests_count = returnRequestsCount(request)   # logic: gets requests count

   context = {'chats': chats, 'chats_count': chats_count, 'requests_count': requests_count}
   return render(request, 'msg-chat.html', context)


def message(request, pk):
   user = User.objects.get(id=pk)
   other_message, other_created = Message.objects.get_or_create(owner=user, recipient = request.user)
   my_message, my_created = Message.objects.get_or_create(owner = request.user, recipient = other_message.owner)

   update_chats_if_settings_says_top_all = checkSettings(request.user, other_message)
   
   # logic: adding the body texts of both users together and filtering them to give a chat fill
   bodys = returnBody(user, request)

   # logic: on message open. make all messages of recipient is_read = True
   messegeSeenUtil(other_message)

   if request.method == "POST":
      # logic: reject empty messages
      reject = rejectEmptyMessageUtil(request.POST['body'])
      if reject: return redirect(message, pk)

      # logic: send request to user-> if friends = requests for both users true. else only one is made true
      sendRequest(user, request.user, other_message, my_message)
      
      body = Body.objects.create(owner=request.user, recipient=other_message.owner, message=my_message, body=request.POST['body'])
      my_message.unread_messages += 1     # logic -> msg.3: increment unread message on my_message to -> recipient
      my_message.save()

      # logic -> msg.3: update both user message objects to the most recent created body in chat -> purpose: all just to display in chats the most recent text and time sent 😪
      my_message.last_body = body
      other_message.last_body = body
      my_message.save()
      updateSubDate(my_message)
      other_message.save()
      updateSubDate(other_message)

      return redirect(message, pk)

   context = {"message": other_message, "bodys": bodys, 'user': user}
   return render(request, 'message.html', context)

def feed(request):
   context = {}
   return render(request, 'msg-feed.html', context)

def friends(request):
   context = {}
   return render(request, 'msg-friends.html', context)


# SECTION 2: Requests & Requests Message
def requests(request):
   chats = request.user.messages.filter(request_accepted = False)
   
   context = {'chats': chats}
   return render(request, 'requests.html', context)

def requestMessage(request, pk):
   user = User.objects.get(id=pk)
   bodys = returnBody(user, request)
   # logic: mark messages as seen
   other_message, other_created = Message.objects.get_or_create(owner=user, recipient = request.user)
   my_message, my_created = Message.objects.get_or_create(owner = request.user, recipient = other_message.owner)
   messegeSeenUtil(other_message)
   if other_message.request_accepted == True and my_message.request_accepted == True:
      return redirect(message, pk)
   

   context = {'user': user, 'bodys': bodys}
   return render(request, 'request-message.html', context)

def acceptRequest(request, pk):
   user = User.objects.get(id=pk)
   other_message, other_created = Message.objects.get_or_create(owner=user, recipient = request.user)
   my_message, my_created = Message.objects.get_or_create(owner = request.user, recipient = other_message.owner)
   acceptRequestUtil(other_message, my_message)
   return redirect(message, pk)

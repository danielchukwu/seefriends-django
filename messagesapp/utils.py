from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Body, Message

from django.db.models import Q


# create your utils here

def sendRequest(user, me, other_message, my_message):
   if user in me.profile.friends.all():
      other_message.request_accepted = True
      my_message.request_accepted = True
      other_message.save()
      my_message.save()
   else:
      other_message.request_accepted = True
      other_message.save()

def acceptRequestUtil(other_message, my_message):
   other_message.request_accepted = True
   my_message.request_accepted = True
   other_message.save()
   my_message.save()

def updateSubDate(message):
   message.subdate = message.updated
   message.save()

def messegeSeenUtil(other_message):
   # logic: mark unread body's as read on message open
   unread_messages = other_message.body_set.filter(is_read = False)
   if unread_messages.count() > 0:
      for msg in unread_messages:
         msg.is_read = True
         msg.save()

   # logic: set unread_messages back to 0
   if other_message.unread_messages > 0:
      other_message.unread_messages = 0
      other_message.subdate = other_message.updated
      other_message.save()

def returnBody(user, request):
   bodys = Body.objects.filter(
      Q (Q (owner = user) & Q (recipient = request.user)) |
      Q (Q (owner = request.user) & Q (recipient = user))
   ).order_by('created')

   return bodys

# SECTION 2: Counts
def returnChatsCount(request):
   chats_count = request.user.messages.filter(
      Q (unread_messages__gt = 0) &
      Q (request_accepted = True)).count()

   return chats_count

def returnChatsCountApi(user):
   chats_count = user.messages.filter(
      Q (unread_messages__gt = 0) &
      Q (request_accepted = True)).count()

   return chats_count

def returnRequestsCount(request):
   requests_count = request.user.messages.filter(
      Q (unread_messages__gt = 0) &
      Q (request_accepted = False)).count()

   return requests_count

# SECTION 3: Empty Message Rejection
def rejectEmptyMessageUtil(message):
   spaces_count = 0
   for each in message:
      if each == " ":
         spaces_count += 1
      else:
         break
   if spaces_count == len(message):
      return True


# SECTION 4: Settings
def returnChats(request):
   "Check in with settings to know the order of the chats wanted"
   if request.user.settings.top_unread == True or request.user.settings.top_all == True:
      chats = request.user.messages.exclude(request_accepted = False)
   else:
      chats = request.user.messages.exclude(request_accepted = False).order_by('-subdate')
   
   return chats

def checkSettings(user, other_message):
   "we order by chats by other_message(not my_message). thats why we save other_message"
   if user.settings.top_all == True:
      other_message.save()
import random
from homeapp.api.serializers import PostSerializer, TellSerializer, UserSerializer
from homeapp.forms import PostForm
from homeapp.utils import returnInterestedFollowings, returnPostsForFeed

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from homeapp.models import Post, Tell

# create your api views here

@api_view(['GET'])
def getRoutes(requet):
   routes = [
      {'GET': '/api/posts'},
      {'GET' : '/api/posts/:id'},
      {'PUT' : '/api/posts/:id'},
      {'POST' : '/api/posts'},

      {'POST' : '/api/users/token'},
      {'POST' : '/api/users/token/refresh'},
   ]

   return Response(routes)

# GETTING POSTS & TELLS and also ["GET", "POST"]
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def getPosts(request):
   if (request.method == "GET"):
      # posts = Post.objects.all()

      "NOTE: its an amazing algorithm no need to write a new one. all you need is to update it with whatever you want whenever"
      userfollows = request.user.profile.following.all()  # print(f"following: {userfollows}")

      # obj 1: get interested followings
      interestedfollowings = returnInterestedFollowings(request, userfollows) # print(f"Views.. {interestedfollowings}")

      # obj 2: get post of interested followings
      unseen, seen = returnPostsForFeed(request, interestedfollowings)

      # obj 3: just because i don't have alot of users posting right now
         # random.shuffle(unseen)
      # random.shuffle(seen)
      posts = unseen + seen

      serializer = PostSerializer(posts, many=True)
      return Response(serializer.data)


   elif (request.method == "POST"):
      Post.objects.create(
         owner = request.user,
         img = request.data['img'],
         body = request.data['body']
      )
      return Response({"message":"successful"})

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def getPost(request, pk):
   post = Post.objects.get(id=pk)
   print("Post:", post)
   serializer = PostSerializer(post, many=False)
   return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def getTells(request):
   if (request.method == "GET"):
      # tells = Tell.objects.all()
      # serializer = TellSerializer(tells, many=True)
      # return Response(serializer.data)

      tells = Tell.objects.all().order_by("-created")
   
      user = request.user
      userfollows = user.profile.following.all()
      # print(f"following: {userfollows}")

      for tell in user.tell_set.all()[:1]:
         if tell not in user.profile.seen_tell.all():
            user.profile.seen_tell.add(tell)
      
      # logic: iterate over people user follows to get thier current post and old post
      seen = user.profile.seen_tell.all()
      for user in userfollows:
         # print(f"\nIteration: {user}")
         following_tell = Tell.objects.filter(owner = user)[:5]
         # user_tell = request.user.tell_set.all()
         for tell in following_tell:
            # print(f"feed tells: {tell}")
            if tell not in seen:
               request.user.profile.seen_tell.add(tell)

      serializer = TellSerializer(tells, many=True)
      return Response(serializer.data)
      
   elif (request.method == "POST"):
      Tell.objects.create(
         owner = request.user,
         body = request.data['body']
      )
      return Response({"message":"successful"})

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def getTell(request, pk):
   tell = Tell.objects.get(id=pk)
   serializer = TellSerializer(tell, many=False)
   return Response(serializer.data)

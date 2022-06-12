from django.db.models import Q
from multiprocessing import context
import random
from homeapp.api import serializers
from homeapp.api.serializers import CommentPostSerializer, CommentTellSerializer, PostSerializer, PostSingleSerializer, ProfileSerializer, SearchSerializer, TellSerializer, TellSingleSerializer, UserSerializer
from homeapp.forms import PostForm
from homeapp.utils import returnInterestedFollowings, returnPostsForFeed

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from homeapp.models import Activity, CommentOnPost, CommentOnTell, Post, Search, Tell
from users.models import Profile
from django.contrib.auth.models import User


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

      serializer = PostSerializer(posts, many=True, context={'request': request}) # PASSING: CONTEXT TO OUR SERIALIZER
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
   serializer = PostSingleSerializer(post, many=False, context={'request': request})
   return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def getTells(request):
   if (request.method == "GET"):
      tells = Tell.objects.all().order_by("-created")
      user = request.user
      userfollows = user.profile.following.all()

      for tell in user.tell_set.all()[:1]:
         if tell not in user.profile.seen_tell.all():
            user.profile.seen_tell.add(tell)
      
      # logic: iterate over people user follows to get thier current post and old post
      seen = user.profile.seen_tell.all()
      for user in userfollows:
         following_tell = Tell.objects.filter(owner = user)[:5]
         for tell in following_tell:
            if tell not in seen:
               request.user.profile.seen_tell.add(tell)

      serializer = TellSerializer(tells, many=True, context={'request': request})
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
   serializer = TellSingleSerializer(tell, many=False, context={'request': request})
   return Response(serializer.data)


# LIKES
# Handle post like and dislike
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def likePost(request, pk):
   post = Post.objects.get(id=pk)
   participants = post.likers.all()
   if request.user not in participants:
      post.likers.add(request.user)
      activity, created = Activity.objects.get_or_create(owner=post.owner, user=request.user, activity_type="like_post", post=post, liker_post=request.user)
      if created:
         post.owner.profile.activity_count = post.owner.profile.activity_count + 1
         post.owner.profile.save()
      return Response({"details": "like successful!"})
   else: 
      user = request.user
      post = Post.objects.get(id=pk)
      participants = post.likers.all()
      if user in participants:
         post.likers.remove(user)
         post.save()
      return Response({"details": "unlike successful!"})

# Handle tell like and dislike
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def likeTell(request, pk):
   tell = Tell.objects.get(id=pk)
   participants = tell.likers.all()
   if request.user not in participants:
      tell.likers.add(request.user)
      activity, created = Activity.objects.get_or_create(owner=tell.owner, user=request.user, activity_type="like_tell", tell=tell, liker_tell=request.user)
      if created:
         tell.owner.profile.activity_count = tell.owner.profile.activity_count + 1
         tell.owner.profile.save()
      return Response({"details": "like successful!"})
   else:
      user = request.user
      tell = Tell.objects.get(id=pk)
      participants = tell.likers.all()
      if user in participants:
         tell.likers.remove(user)
         tell.save()
      return Response({"details": "unlike successful!"})


# Comments: Post and Tells
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def commentOnPost(request, pk):
   post_object = Post.objects.get(id=pk)
   post_object.commenters.add(request.user)
   post_object.save()
   if request.method == "POST":
      user = request.user
      add_comment = request.data["body"]
      comment = CommentOnPost.objects.create(
         owner = user,
         post = post_object,
         comment = add_comment
      )
      activity, created = Activity.objects.get_or_create(owner=post_object.owner, user=request.user, activity_type="comment_post", post=post_object, comment_post=comment)
      if created:
         post_object.owner.profile.activity_count += 1
         post_object.owner.profile.save()
   
   serializer = CommentPostSerializer(comment, many=False)

   return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def commentOnTell(request, pk):
   tell_object = Tell.objects.get(id=pk)
   if request.method == "POST":
      user = request.user
      add_comment = request.data["body"]
      comment = CommentOnTell.objects.create(
         owner = user,
         tell = tell_object,
         comment = add_comment
      )
      activity, created = Activity.objects.get_or_create(owner=tell_object.owner, user=request.user, activity_type="comment_tell", tell=tell_object, comment_tell=comment)
      if created:
         tell_object.owner.profile.activity_count += 1
         tell_object.owner.profile.save()
      
   serializer = CommentTellSerializer(comment, many=False)

   return Response(serializer.data)

# Post and Tell: Event actions: save, tell on, msg
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def savePost(request, pk):
   post = Post.objects.get(id=pk)
   if post not in request.user.profile.saved_post.all():
      request.user.profile.saved_post.add(post)
      post.savers.add(request.user)
   else: 
      request.user.profile.saved_post.remove(post)
      post.savers.add(request.user)
   
   return Response({"details": "successful!"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saveTell(request, pk):
   tell = Tell.objects.get(id=pk)
   if tell not in request.user.profile.saved_tell.all():
      request.user.profile.saved_tell.add(tell)
      tell.savers.add(request.user)
   else: 
      request.user.profile.saved_tell.remove(tell)
      tell.savers.remove(request.user)
   
   return Response({"details": "successful!"})


# tell On Post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tellOnPost(request, pk):
   print("Telling On Post")
   post = Post.objects.get(id=pk)
   print(post)

   # tell creation
   Tell.objects.create(
         owner = request.user,
         body = request.data['body'],
         type = "post",
         tell_on_post = post
      )

   # update the post that we are telling on
   post.tellers.add(request.user)
   post.tellers_count += 1
   post.save()
   
   return Response({"details": "successful!"})

# tell on Tell
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tellOnTell(request, pk):
   tell = Tell.objects.get(id=pk)
   # tell creation
   created_tell = Tell.objects.create(
         owner = request.user,
         body = request.data['body'],
         type = "tell",
         tell_on_tell = tell
      )
   
   # update the tell that we are telling on
   tell.tellers.add(request.user)
   tell.tellers_count += 1
   tell.save()

   serializer = TellSerializer(created_tell, many=False, context={'request': request})
   
   return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def discover(request):
   post = sorted(Post.objects.all(), key=lambda x: random.random())[:22]
   print(len(post))
   # print(type(post))
   serializer = PostSerializer(post, many=True, context={"request": request})
   return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def search(request):
   if (request.method == "GET"):
      searchs = Search.objects.filter(owner=request.user) 

      serializer = SearchSerializer(searchs, many= True)
      return Response(serializer.data)
   elif (request.method == "POST"):
      print("IN SEARCH...................")
      print(request.data)
      print(request.data['body'])
      # search = request.data['body'] if request.data['body'] != None else '   '
      search = request.data['body']

      users = User.objects.filter(
         Q(username__startswith = search) |
         Q(first_name__startswith = search) 
      )

      # users = User.objects.filter(
      #    Q(username__icontains = search) |
      #    Q(first_name__icontains = search)
      # )

      serializer = UserSerializer(users, many=True)
      return Response(serializer.data)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def addSearchProfile(request, pk):


   if (request.method == "GET"): # GET pk: should be user id
      search, created = Search.objects.get_or_create(owner=request.user, user=User.objects.get(id=pk))
      if created: 
         print(f'Search Created: {search}')
      else: search.save()
      return Response({"details": "successful!"})
   elif (request.method == "DELETE"): # DELETE pk: should be search id
      search = Search.objects.get(id=pk)
      search.delete()
      new_searchs = request.user.search_set.all()
      serializer = SearchSerializer(new_searchs, many= True)

      return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPostThreads(request, pk):
   post = Post.objects.get(id=pk)
   tells = post.tell_on_post.all()
   serializer = TellSerializer(many=True)
   # return Response({"details": "successful!"})
   return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTellThreads(request, pk):
   tell = Tell.objects.get(id=pk)
   tells = tell.tell_on_tell.all()
   serializer = TellSerializer(many=True)
   # return Response({"details": "successful!"})
   return Response(serializer.data)


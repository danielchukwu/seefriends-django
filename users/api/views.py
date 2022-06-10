from multiprocessing import context
from users.forms import CustomUserCreationForm, UpdateProfileForm
from users.models import Profile, UserFollower, UserFollowing
from users.utils import checkRegistration, checkUpdate
from .serializers import ActivitySerializer, PostSerializer, TellSerializer, UserSerializer
from homeapp.models import Activity, Post, PostFeed, Tell, SavePost, SaveTell

from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.api import serializers


# create your user views here


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOwner(request):
   user = request.user
   serializer= UserSerializer(user, many=False)
   return Response(serializer.data)

# Activity
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getActivities(request):
   if (request.user):
      profile = request.user.profile
      profile.activity_count = 0
      profile.save()
      print(f"Activity Count: {profile.activity_count}")
   activities = request.user.activity_set.all()
   # print(activities)
   serializer = ActivitySerializer(activities, many=True)
   return Response(serializer.data)

# User Profile
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getUser(request, pk):
   user = User.objects.get(id=pk)
   serializer = UserSerializer(user, many=False)
   return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserPost(request, pk):
   user = User.objects.get(id=pk)
   posts = user.post_set.all()
   serializer = PostSerializer(posts, many=True, context={'request': request})
   return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserTells(request, pk):
   user = User.objects.get(id=pk)
   tells = user.tell_set.all()
   print("tells:", tells)
   serializer = TellSerializer(tells, many=True, context={'request': request})
   return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSavedPosts(request):
   if (request.method == "GET"):
      saved_post = request.user.profile.saved_post.all()
      print(saved_post)
      serializer = PostSerializer(saved_post, many=True, context={'request': request})
      # print("saved_post:", saved_post)
      return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSavedTells(request):
   saved_tell = request.user.profile.saved_tell.all()
   serializer = TellSerializer(saved_tell, many=True, context={'request': request})
   # print("saved_tell:", saved_tell)
   return Response(serializer.data)


# fff
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFollowers(request, pk):
   followers = User.objects.get(id=pk).profile.followers.all()
   serializer = UserSerializer(followers, many=True)
   # print("followers:", followers)
   return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFollowings(request, pk):
   followings = User.objects.get(id=pk).profile.following.all()
   serializer = UserSerializer(followings, many=True)
   # print("followings:", followings)
   return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFriends(request, pk):
   friends = User.objects.get(id=pk).profile.friends.all()
   serializer = UserSerializer(friends, many=True)
   # print("friends:", friends)
   return Response(serializer.data)


# Follow & Unfollow logic
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def follow(request, pk):
   # logic: user & profile
   user = User.objects.get(id=pk)   # user to be followed
   profile = user.profile           # user to be followed profile

   # stop if user === request.user
   if user == request.user:
      return Response(["can't follow yourself!"])
   elif request.user in profile.followers.all():
      return Response(["already following!"])

   # start following
   profile.followers.add(request.user)       # user->profile-> become a follower
   request.user.profile.following.add(user)  # request.user->profile-> start following

   # logic: if both users are following each other -> become friends :: This is gr8 commenting nonso. I won't lie😉👍
   friends = False
   if request.user in profile.following.all():
      request.user.profile.friends.add(user)
      profile.friends.add(request.user)
      friends = True

   # logic: create following and follower model
   UserFollowing.objects.create(
      me = request.user,
      following = user
   )

   UserFollower.objects.create(
      me = request.user,
      follower_to = user,
   )

   if friends:
      otheru_activity, created1 = Activity.objects.get_or_create(owner=user, user=request.user, activity_type="friends")  # Activity for the person followed
      my_activity, created2 = Activity.objects.get_or_create(owner=request.user, user=user, activity_type="friends")  # Activity for you the follower
      if created1: 
         profile.activity_count += 1  # increment the activity count of the person followed
         profile.save()
      if created2: 
         request.user.profile.activity_count += 1  # increment the activity count for you the follower
         request.user.profile.save()
   
   else:
      otheru_activity, created1 = Activity.objects.get_or_create(owner=user, user=request.user, activity_type="follow")
      if created1: 
         profile.activity_count = profile.activity_count + 1
         profile.save()
   
   return Response({"details":"successful!"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unfollow(request, pk):
   # logic: user & profile
   user = User.objects.get(id=pk)    # user to be followed
   profile = user.profile            # user to be followed profile

   # stop if user === request.user
   if user == request.user:
      return Response(["can't follow yourself!"])
   elif request.user not in profile.followers.all():
      return Response(["not following already!"])
   
   # start unfollowing
   profile.followers.remove(request.user)       # user->profile-> in user unfollow
   request.user.profile.following.remove(user)  # request.user->profile-> in request.user unfollow

   # logic: if a user is not following the other -> remove friendship
   if request.user in profile.friends.all():
      profile.friends.remove(request.user)
      request.user.profile.friends.remove(user)
   
   # logic: delete following and follower model
   following_model = UserFollowing.objects.get(me = request.user, following = user)
   following_model.delete()

   follower_model = UserFollower.objects.get(me = request.user, follower_to = user)
   follower_model.delete()

   # Logic: delete postsfeed and remove posts from seen
   post_feed = PostFeed.objects.filter(post_owner=user)
   for each_feed in post_feed:
      request.user.profile.seen_post.remove(each_feed.post)
      each_feed.delete()
   
   return Response({"details":"successful!"})


@api_view(["POST"])
def registerUser(request):
   page = 'register'
   form = CustomUserCreationForm()
   print(request.data)

   username = request.data['username']
   email = request.data['email']
   password1 = request.data['password1']
   password2 = request.data['password2']

   # sanity check
   # all errors = username, email, passwords unexact, password similar, password short, password easy 
   check = checkRegistration(username, email, password1, password2)
   print("Invalidated:",check)
   if (check):
      return Response({'errors': check})
   
   if request.method == "POST":
      form = CustomUserCreationForm(request.data)
      if form.is_valid():
         print("form is valid")
         user = form.save(commit=False)
         user.first_name = user.first_name.lower()
         user.username = user.username.lower()
         user.save()

         return Response({'details': 'successful!'})
      else:
         print(form.errors)
         check.append('password easy')
         return Response({'errors': check})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def updateProfile(request):
   user = request.user
   form = UpdateProfileForm(instance=user.profile)
   if request.method == "POST":
      username = request.data['username']
      email = request.data['email']
      password1 = "dan12345"
      password2 = "dan12345"

      check = checkUpdate(request, username, email)
      print("Invalidated:",check)
      if (check):
         return Response({'errors': check})
      
      form = UpdateProfileForm(request.POST, request.FILES, instance=user.profile)
      if form.is_valid():
         profile = form.save()
         return Response({'details': "successful!"})
      else:
         print(form.errors)
         return Response({'details': "unsuccessful!"})
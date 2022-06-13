from os import remove
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from homeapp.models import Activity, Post, PostFeed, Tell, SavePost, SaveTell

from homeapp.views import home, tellsPage
from messagesapp.utils import *
from .forms import CustomUserCreationForm, UpdateProfileForm

# Create your views here.
from .models import Profile, UserFollower, UserFollowing
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# SECTION 1: USER PROFILE & OTHER USER PROFILE -> Landing Page
@login_required(login_url="login")
def userProfile(request):
   page = "user-post"
   user = request.user
   contents = user.post_set.all()
   chats_count = returnMessagesCount(request)     # logic: gets chats count

   context = {'user': user, 'contents': contents, 'chats_count': chats_count, 'page': page}
   return render(request, 'user-profile.html', context)

@login_required(login_url="login")
def userProfileTells(request):
   page = "user-tell"
   user = request.user
   contents = user.tell_set.all()
   chats_count = returnMessagesCount(request)     # logic: gets chats count

   context = {'user': user, 'contents': contents, 'chats_count': chats_count, 'page': page}
   return render(request, 'user-profile.html', context)

@login_required(login_url="login")
def otherProfile(request, pk):
   page = "user-post"
   user = User.objects.get(id=pk)
   if user == request.user: return redirect(userProfile)
   contents = user.post_set.all()
   chats_count = returnMessagesCount(request)     # logic: gets chats count

   context = {'user': user, 'contents': contents, 'chats_count': chats_count, 'page': page}
   return render(request, 'user-profile.html', context)

def otherProfileTells(request, pk):
   page = "user-tell"
   user = User.objects.get(id=pk)
   if user == request.user: return redirect(userProfileTells)
   contents = user.tell_set.all()
   chats_count = returnMessagesCount(request)     # logic: gets chats count

   context = {'user': user, 'contents': contents, 'chats_count': chats_count, 'page': page}
   return render(request, 'user-profile.html', context)


# SECTION 2: FOLLOW & UNFOLLOW -> algorithm
@login_required(login_url="login")
def follow(request, pk):
   # logic: user & profile
   user = User.objects.get(id=pk)   # user to be followed
   profile = user.profile           # user to be followed profiled

   if request.user in profile.followers.all():
      return
   
   # stop if user === request.user
   if user == request.user:
      return redirect(request.GET["q"])
   elif request.user in profile.followers.all():
      return redirect(request.GET["q"])
      

   # start following
   profile.followers.add(request.user)       # user->profile-> become a follower
   request.user.profile.following.add(user)  # request.user->profile-> start following

   # logic: if both both users are following each other -> become friends
   if request.user in profile.following.all():
      request.user.profile.friends.add(user)
      profile.friends.add(request.user)

   # logic: create following and follower model
   UserFollowing.objects.create(
      me = request.user,
      following = user
   )

   UserFollower.objects.create(
      me = request.user,
      follower_to = user,
   )

   Activity.objects.get_or_create(owner=user, user=request.user, activity_type="follow")
   profile.activity_count = profile.activity_count + 1
   profile.save()
   # print(f"ACTIVITY_COUNT: {profile.activity_count}")

   try:
      if request.GET['q']:
         return redirect(request.GET['q'])
      else:
         return redirect(otherProfile, pk)
   except:
      return redirect(otherProfile, pk)


@login_required(login_url="login")
def unfollow(request, pk):
   user = User.objects.get(id=pk)    # user to be followed
   profile = user.profile            # user to be followed profiled

   if request.user not in profile.followers.all():
      return
   
   # logic: user->profile-> stop following and remove user as follower
   profile.followers.remove(request.user)       # user->profile-> in user unfollow
   request.user.profile.following.remove(user)  # request.user->profile-> in request.user unfollow

   # logic: if a user is not following the other -> remove friendship
   if request.user in profile.friends.all():
      request.user.profile.friends.remove(user)
      profile.friends.remove(request.user)
   
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
   
   try:
      if request.GET['q']:
         return redirect(request.GET['q'])
      else:
         return redirect(otherProfile, pk)
   except:
      return redirect(otherProfile, pk)


# SECTION 3: AUTHENTICATION -> & Log in, Log out and Registration
def loginUser(request):
   page = "login"
   if request.method == "POST":
      # print(f"LOGIN: {request.POST}")
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(request, username=username, password=password)
      # print(f"USER STATUS: {user}")
      if user:
         login(request, user)
         return redirect(home)
      else:
         print("incorrect info")

   context = {"page": page}
   return render(request, 'login-reg-form.html', context)

@login_required(login_url="login")
def logoutUser(request):
   logout(request)
   return redirect(loginUser)


def registerUser(request):
   page = 'register'
   form = CustomUserCreationForm()
   if request.method == "POST":
      form = CustomUserCreationForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.first_name = user.first_name.lower()
         user.username = user.username.lower()
         user.save()
         login(request, user)
         return redirect(home)
   
   context={"page": page, "form": form}
   return render(request, 'login-reg-form.html', context)



# SECTION 4: updateProfile
def updateProfile(request):
   user = request.user
   form = UpdateProfileForm(instance=user.profile)
   if request.method == "POST":
      # reject if a username is in use:
      username_exist = Profile.objects.filter(username__exact=request.POST['username'])
      # print(f"Profile:{username_exist}")
      
      form = UpdateProfileForm(request.POST, request.FILES, instance=user.profile)
      if form.is_valid():
         profile = form.save()
         return redirect(userProfile)
   context = {"form": form}
   return render(request, 'update-profile.html', context)


# SECTION 5: SAVE Posts & Tells
# 1. POST
def savedPostPage(request):
   page = "post"
   user = request.user
   saved_posts = user.savepost_set.all().order_by('-updated')

   context = {"page": page, "contents": saved_posts}
   return render(request, 'saved.html', context)

def savePost(request, pk):
   user = request.user
   save_post = Post.objects.get(id=pk)
   SavePost.objects.create(
      owner = user,
      post = save_post
   )

   # add id to profile as saved
   user.profile.saved_post.add(save_post)

   return redirect(savedPostPage)

def unsavePost(request, pk):
   user = request.user
   remove_post = Post.objects.get(id=pk)
   post = SavePost.objects.get(owner=user, post=remove_post)
   # print(f"Post b4 delete: {post}")
   post.delete()
   # print(f"Post af delete: {post}")
   user.profile.saved_post.remove(remove_post)

   return redirect(savedPostPage)




# 2. TELL
def savedTellPage(request):
   page = "tell"
   user = request.user
   saved_tells = user.savetell_set.all().order_by('-updated')

   context = {"page": page, "contents": saved_tells}
   return render(request, 'saved.html', context)

def saveTell(request, pk):
   user = request.user
   save_tell = Tell.objects.get(id=pk)
   SaveTell.objects.create(
      owner = user,
      tell = save_tell
   )

   # add id to profile as saved
   user.profile.saved_tell.add(save_tell)
   
   return redirect(savedTellPage)

def unsaveTell(request, pk):
   user = request.user
   remove_tell = Tell.objects.get(id=pk)
   tell = SaveTell.objects.get(owner=user, tell=remove_tell)
   # print(f"tell b4 delete: {tell}")
   tell.delete()
   # print(f"tell af delete: {tell}")
   user.profile.saved_tell.remove(remove_tell)

   return redirect(savedTellPage)




# SECTION 6: PAGE OF => FOLLOWERS, FOLLOWING, FRIENDS
def followersPage(request, pk):
   page = 'followers'
   user = User.objects.get(id=pk)
   followers = UserFollower.objects.filter(follower_to = user)
   # print(f"Followers: {followers}")

   context = {'page': page, 'user': user, 'followers': followers}
   return render(request, 'fff.html', context)




def followingPage(request, pk):
   page = 'following'
   user = User.objects.get(id=pk)
   following = UserFollowing.objects.filter(me = user)
   # print(f"Following: {following}")

   context = {'page': page, 'user': user, 'following': following}
   return render(request, 'fff.html', context)




def friendsPage(request, pk):
   page = 'friends'
   user = User.objects.get(id=pk)
   friends = user.profile.friends.all()
   # print(f"Friends: {friends}")
   
   context = {'page': page, 'user': user, 'friends': friends}
   return render(request, 'fff.html', context)



# SECTION 7: ACTIVITY PAGE............
def activityPage(request):
   profile = request.user.profile
   profile.activity_count = 0
   profile.save()
   # print(f"Activity Count: {profile.activity_count}")
   chats_count = returnMessagesCount(request)     # logic: gets chats count
   
   context = {'chats_count': chats_count}
   return render(request, 'activity.html', context)
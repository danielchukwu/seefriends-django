from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from homeapp.models import Post, Tell, SavePost, SaveTell

from homeapp.views import home, tellsPage
from .forms import CustomUserCreationForm, UpdateProfileForm

# Create your views here.
from .models import Profile
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# SECTION 1: USER PROFILE & OTHER USER PROFILE -> Landing Page
@login_required(login_url="login")
def userProfile(request):
   user = request.user
   contents = user.post_set.all()

   context = {'user': user, 'contents': contents}
   return render(request, 'user-profile.html', context)

@login_required(login_url="login")
def userProfileTells(request):
   user = request.user
   contents = user.tell_set.all()

   context = {'user': user, 'contents': contents}
   return render(request, 'user-profile.html', context)

@login_required(login_url="login")
def otherProfile(request, pk):
   user = User.objects.get(id=pk)
   if user == request.user: return redirect(userProfile)
   contents = user.post_set.all()

   context = {'user': user, 'contents': contents}
   return render(request, 'user-profile.html', context)

def otherProfileTells(request, pk):
   user = User.objects.get(id=pk)
   if user == request.user: return redirect(userProfileTells)
   contents = user.tell_set.all()

   context = {'user': user, 'contents': contents}
   return render(request, 'user-profile.html', context)



# SECTION 2: FOLLOW & UNFOLLOW -> algorithm
@login_required(login_url="login")
def follow(request, pk):
   # logic: user & profile
   user = User.objects.get(id=pk)   # user to be followed
   profile = user.profile           # user to be followed profiled

   # start following
   profile.followers.add(request.user)       # user->profile-> become a follower
   request.user.profile.following.add(user)  # request.user->profile-> start following

   # logic: if both both users are following each other -> become friends
   if request.user in profile.following.all():
      request.user.profile.friends.add(user)
      profile.friends.add(request.user)
      # print(f"{request.user} friends:", request.user.profile.friends.all())
      # print(f"{user} friends:", profile.friends.all())
   else:
      print("Not following you")

   return redirect(otherProfile, pk)

@login_required(login_url="login")
def unfollow(request, pk):
   user = User.objects.get(id=pk)    # user to be followed
   profile = user.profile            # user to be followed profiled
   
   # logic: user->profile-> stop following
   profile.followers.remove(request.user)       # user->profile-> in user unfollow
   request.user.profile.following.remove(user)  # request.user->profile-> in request.user unfollow

   # logic: if a user is not following the other -> remove friendship
   if request.user in profile.friends.all():
      request.user.profile.friends.remove(user)
      profile.friends.remove(request.user)
      # print(f"{request.user} friends:", request.user.profile.friends.all())
      # print(f"{user} friends:", profile.friends.all())
   else:
      print("Not following you")

   return redirect(otherProfile, pk)



# SECTION 3: AUTHENTICATION -> & Log in, Log out and Registration
def loginUser(request):
   page = "login"
   if request.method == "POST":
      # print(f"LOGIN: {request.POST}")
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(request, username=username, password=password)
      print(f"USER STATUS: {user}")
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
      print(f"Profile:{username_exist}")
      
      form = UpdateProfileForm(request.POST, request.FILES, instance=user.profile)
      if form.is_valid():
         form.save()
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


# 2. TELL
def savedTellPage(request):
   page = "tell"
   user = request.user
   saved_tells = user.savetell_set.all()


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

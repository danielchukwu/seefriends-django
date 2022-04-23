import imp
from importlib.resources import contents
from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from homeapp.forms import PostForm
from messagesapp.utils import returnChatsCount
from users.models import Profile

# Create your views here.
from .models import Activity, CommentOnPost, Post, Search, Tell, CommentOnTell
from itertools import chain
import random

from .utils import *

# 
# 
# 
# 
# SECTION 1: TELL
@login_required(login_url="login")
def tellsPage(request):
   tells = Tell.objects.all().order_by("-created")
   
   user = request.user
   userfollows = user.profile.following.all()
   # print(f"following: {userfollows}")

   for tell in request.user.tell_set.all()[:1]:
      if tell not in user.profile.seen_tell.all():
         user.profile.seen_tell.add(tell)
   
   # logic: iterate over people user follows to get thier current post and old post
   seen = request.user.profile.seen_tell.all()
   for user in userfollows:
      # print(f"\nIteration: {user}")
      following_tell = Tell.objects.filter(owner = user)[:5]
      # user_tell = request.user.tell_set.all()
      for tell in following_tell:
         # print(f"feed tells: {tell}")
         if tell not in seen:
            request.user.profile.seen_tell.add(tell)

   # logic: chats count to display chat count
   chats_count = returnChatsCount(request)     # logic: gets chats count

   context = {'tells': request.user.profile.seen_tell.all(), 'chats_count': chats_count}
   return render(request, 'tells.html', context)

# like
@login_required(login_url="login")
def likeTell(request, pk):
   tell = Tell.objects.get(id=pk)
   participants = tell.likers.all()
   # print("Like\n", participants)
   if request.user not in participants:
      tell.likers.add(request.user)
      activity, created = Activity.objects.get_or_create(owner=tell.owner, user=request.user, activity_type="like_tell", tell=tell, liker_tell=request.user)
      if created:
         tell.owner.profile.activity_count = tell.owner.profile.activity_count + 1
         tell.owner.profile.save()
         print(f"ACTIVITY_COUNT: {tell.owner.profile.activity_count}")

   return redirect(request.GET['q'])

# unlike
@login_required(login_url="login")
def unlikeTell(request, pk):
   user = request.user
   tell = Tell.objects.get(id=pk)
   participants = tell.likers.all()
   # print("Unlike\n", participants)
   if user in participants:
      tell.likers.remove(user)
      # print("Unlike\n", participants)
      tell.save()
   
   return redirect(request.GET['q'])

# tell form
@login_required(login_url="login")
def tellForm(request):
   user = request.user
   if request.method == "POST":
      tell = Tell.objects.create(
         owner = user,
         body = request.POST.get('tell')
      )
      return redirect(tellsPage)
   
   # logic: chats count to display chat count
   chats_count = returnChatsCount(request)     # logic: gets chats count

   context = {'chats_count': chats_count}
   return render(request, 'tell-form.html', context)

# comments page
@login_required(login_url="login")
def tellCommentsPage(request, pk):
   tell = Tell.objects.get(id=pk)
   context = {'tell': tell}
   return render(request, 'comment.html', context)

# make comment
@login_required(login_url="login")
def addTellComment(request, pk):
   tell_object = Tell.objects.get(id=pk)
   if request.method == "POST":
      user = request.user
      add_comment = request.POST["comment"]
      # print("COMMENT:", add_comment)
      if len(add_comment) == 0:
         return redirect('tell-comments-page', pk)
      comment = CommentOnTell.objects.create(
         owner = user,
         tell = tell_object,
         comment = add_comment
      )
      activity, created = Activity.objects.get_or_create(owner=tell_object.owner, user=request.user, activity_type="comment_tell", tell=tell_object, comment_tell=comment)
      if created:
         tell_object.owner.profile.activity_count = tell_object.owner.profile.activity_count + 1
         tell_object.owner.profile.save()
         print(f"ACTIVITY_COUNT: {tell_object.owner.profile.activity_count}")

   return redirect('tell-comments-page', pk)


# 
# 
# 
# 
# 
# SECTION 2: POST

# POST
@login_required(login_url="login")
def home(request):
   "NOTE: its an amazing algorithm no need to write a new one. all you need is to update it with whatever you want whenever"
   userfollows = request.user.profile.following.all()  # print(f"following: {userfollows}")

   # obj 1: get interested followings
   interestedfollowings = returnInterestedFollowings(request, userfollows) # print(f"Views.. {interestedfollowings}")

   # obj 2: get post of interested followings
   unseen, seen = returnPostsForFeed(request, interestedfollowings)

   # obj 3: just because i don't have alot of users posting right now
      # random.shuffle(unseen)
   random.shuffle(seen)
   contents = unseen + seen

   chats_count = returnChatsCount(request)     # logic: gets chats count
   
   context = {'contents': contents, 'chats_count': chats_count}
   return render(request, 'home.html', context)


def singlePostPage(request, pk):
   page = "post"
   post = Post.objects.get(id=pk)
   context = {'page': page, 'content': post}
   return render(request, 'singles-page.html', context)

def singleTellPage(request, pk):
   tell = Tell.objects.get(id=pk)
   context = {'content': tell}
   return render(request, 'singles-page.html', context)


# like
@login_required(login_url="login")
def likePost(request, pk):
   post = Post.objects.get(id=pk)
   participants = post.likers.all()
   if request.user not in participants:
      post.likers.add(request.user)
      activity, created = Activity.objects.get_or_create(owner=post.owner, user=request.user, activity_type="like_post", post=post, liker_post=request.user)
      if created:
         post.owner.profile.activity_count = post.owner.profile.activity_count + 1
         post.owner.profile.save()
         print(f"ACTIVITY_COUNT: {post.owner.profile.activity_count}")
      
   return redirect(request.GET['q'])

# ulike
@login_required(login_url="login")
def unlikePost(request, pk):
   user = request.user
   post = Post.objects.get(id=pk)
   participants = post.likers.all()
   # print("Unlike\n", participants)
   if user in participants:
      post.likers.remove(user)
      # print("Unlike\n", participants)
      post.save()
   
   return redirect(request.GET['q'])

# post form
@login_required(login_url="login")
def createPost(request):
   user = request.user
   # print(request.user)
   form = PostForm()
   if request.method == "POST":
      form = PostForm(request.POST, request.FILES)
      if form.is_valid:
         post = form.save(commit=False)
         post.owner = user
         # print(post.owner)
         post.save()
         return redirect(home)
   
   # logic: chats count to display chat count
   chats_count = returnChatsCount(request)     # logic: gets chats count

   context = {'user': user, 'chats_count': chats_count}
   return render(request, 'create-post.html', context)

# comments page
@login_required(login_url="login")
def postCommentsPage(request, pk):
   post = Post.objects.get(id=pk)
   context = {'post': post}
   return render(request, 'post-comment-page.html', context)

# make comment
@login_required(login_url="login")
def addPostComment(request, pk):
   post_object = Post.objects.get(id=pk)
   post_object.commenters.add(request.user)
   post_object.save()
   if request.method == "POST":
      user = request.user
      add_comment = request.POST["comment"]
      if len(add_comment) == 0:
         return redirect('tell-comments-page', pk)
      comment = CommentOnPost.objects.create(
         owner = user,
         post = post_object,
         comment = add_comment
      )
      activity, created = Activity.objects.get_or_create(owner=post_object.owner, user=request.user, activity_type="comment_post", post=post_object, comment_post=comment)
      if created:
         post_object.owner.profile.activity_count = post_object.owner.profile.activity_count + 1
         post_object.owner.profile.save()
         print(f"ACTIVITY_COUNT: {post_object.owner.profile.activity_count}")
      
   return redirect('post-comments-page', pk)




# SECTION 3: Discover page
def discoverPage(request):
   post = sorted(Post.objects.all(), key=lambda x: random.random())
   # print(f"Post: {post}")

   context = {"post": post}
   return render(request, 'discover.html', context)

def searchPage(request):
   #logic: get all the searches that has been clicked on by request.user
   searchs = Search.objects.filter(owner=request.user) 

   search = request.GET.get('search') if request.GET.get('search') != None else '   '

   profiles = Profile.objects.filter(
      Q(username__icontains = search) |
      Q(name__icontains = search)
   )
   

   context = {"profiles": profiles, "searchs": searchs, "sv": search}
   return render(request, 'search.html', context)

def pickedSearch(request, pk):
   search, created = Search.objects.get_or_create(owner=request.user, user=User.objects.get(id=pk))
   if created: print(f'Search Created: {search}')
   else: search.save()
   return redirect('other-profile', pk)

def deleteSearch(request, pk):
   search = Search.objects.get(id=pk)
   search.delete()
   
   return redirect('search')
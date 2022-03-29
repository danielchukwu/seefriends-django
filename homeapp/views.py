from importlib.resources import contents
from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from homeapp.forms import PostForm

# Create your views here.
from .models import CommentOnPost, Post, Tell, CommentOnTell
from itertools import chain
import random

tells = [
   {"id": 1, "tell": "I just saw a blind guy independently buy himself pizza"},
   {"id": 2, "tell": "Who wants to join me on a note worthy trip to my village next week"},
   {"id": 3, "tell": "God is good. I will make it out of this. The Lord is my the strength!"}
]



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
   print(f"following: {userfollows}")

   for tell in request.user.tell_set.all()[:1]:
      if tell not in user.profile.seen_tell.all():
         user.profile.seen_tell.add(tell)
   
   # logic: iterate over people user follows to get thier current post and old post
   seen = request.user.profile.seen_tell.all()
   for user in userfollows:
      print(f"\nIteration: {user}")
      following_tell = Tell.objects.filter(owner = user)[:5]
      # user_tell = request.user.tell_set.all()
      for tell in following_tell:
         # print(f"feed tells: {tell}")
         if tell not in seen:
            request.user.profile.seen_tell.add(tell)
   
   
   # print(f"SEEN: {seen}")

   context = {'tells': request.user.profile.seen_tell.all()}
   return render(request, 'tells.html', context)

# like
@login_required(login_url="login")
def likeTell(request, pk):
   tell = Tell.objects.get(id=pk)
   participants = tell.likers.all()
   # print("Like\n", participants)
   if request.user not in participants:
      tell.likers.add(request.user)
      # print("Like\n", participants)
      tell.save()
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
   # print(request.POST)
   return render(request, 'tell-form.html')

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
      CommentOnTell.objects.create(
         owner = user,
         tell = tell_object,
         comment = add_comment
      )
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
   # posts = Post.objects.all().order_by("-created")
   # tells = Tell.objects.all().order_by("-created")
   # contents = list(chain(posts, tells))

   user = request.user
   userfollows = user.profile.following.all()
   print(f"following: {userfollows}")

   # lists: that will contain the post for user account, and accounts who recently posted and ones whose post is not recent to user
   my_post = []
   for user_post in request.user.post_set.all():
      if user_post not in user.profile.seen_post.all():
         my_post.append(user_post)
         user.profile.seen_post.add(user_post)
   
   new_feed = []
   old_feed = []

   # logic: iterate over people user follows to get thier current post and old post
   for user in userfollows:
      print(f"\nIteration: {user}")
      following_post = Post.objects.filter(owner = user)[:]
      for post in following_post:
         print(f"feed posts: {post}")
         seen_post = user.profile.seen_post.all()
         if post not in seen_post:
            new_feed.append(post)
            user.profile.seen_post.add(post)
         else:
            old_feed.append(post)
   
   # logic: reversing and shuffling the feed
   new_feed.reverse()
   old_feed.reverse()
   random.shuffle(new_feed)
   random.shuffle(old_feed)
   new_feed.extend(old_feed)

   if my_post:
      my_post.extend(new_feed)
      contents = my_post
   else:
      contents = new_feed
   
   context = {'contents': contents}
   return render(request, 'home.html', context)

# like
@login_required(login_url="login")
def likePost(request, pk):
   post = Post.objects.get(id=pk)
   participants = post.likers.all()
   # print("Like\n", participants)
   if request.user not in participants:
      post.likers.add(request.user)
      # print("Like\n", participants)
      post.save()
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
   context = {'user': user}
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
   if request.method == "POST":
      user = request.user
      add_comment = request.POST["comment"]
      # print("COMMENT:", add_comment)
      if len(add_comment) == 0:
         return redirect('tell-comments-page', pk)
      CommentOnPost.objects.create(
         owner = user,
         post = post_object,
         comment = add_comment
      )
   return redirect('post-comments-page', pk)
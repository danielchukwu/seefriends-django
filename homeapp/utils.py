import random

from homeapp.models import Post, PostFeed

# create your utils here

def oldFeedAlgorithm(request, userfollows):
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
      # print(f"\nIteration: {user}")
      following_post = Post.objects.filter(owner = user)[:]
      for post in following_post:
         # print(f"feed posts: {post}")
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

# SECTION 2: Seen
def addToSeenPost(request, post):
   request.user.profile.seen_post.add(post)
   request.user.profile.save()

def returnInterestedFollowings(request, userfollows):
   # part 1: give points to follows whose post you interact with the most
   users_kv = {}
   for user in userfollows:
      users_kv[user] = 0
      user_posts = user.post_set.all().order_by('created')[:5]
      for post in user_posts:   # print(f"{user}.. post -> {post}__________")
         if request.user in post.commenters.all() and request.user in post.likers.all():
            users_kv[user] += 3   # add 3points
         elif request.user in post.likers.all():
            users_kv[user] += 2   # add 2points
         else:
            users_kv[user] += 0   # add 0points
   
   # part 2: sort users by most interested
   users_sbi = sorted(users_kv.items(), key=lambda x:x[1], reverse=True)   # sbi: sorted by interest
         # print(f"Unsorted: {users_kv}\n")
         # print(f"Sorted: {users_sbi}\n")

   users_interestedin = [x[0] for x in users_sbi]
         # print(f"users_interestedin: {users_interestedin}\n")

   return users_interestedin

def returnPostsForFeed(request, interestedfollowings):
   unseen, seen = [], []
   unseen_count, seen_count = 0, 0
   # logic: check if request.user have any unseen post to append to unseen first
   for post in request.user.post_set.all()[:1]:
      if post not in request.user.profile.seen_post.all():
         unseen.append(post)
   
   for user in interestedfollowings:   # print(f"User: {user}")
      for post in user.post_set.all():
         if post not in request.user.profile.seen_post.all():
            unseen.append(post)
            unseen_count +=1
            addToSeenPost(request, post)
         else:
            seen.append(post)
            seen_count +=1
   
   # part 2: logic: create feed of unseen items
   unseen.reverse()
   for post in unseen:   # print(f"FEED READY = {post.is_feed_ready}")
      if post.is_feed_ready:
         post, created = PostFeed.objects.get_or_create(owner=request.user, post_owner=post.owner, post=post)
      else: continue
   unseen.reverse()  # print(unseen)
   
   return unseen, seen


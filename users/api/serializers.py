from dataclasses import field
from operator import mod
from homeapp.models import Activity, CommentOnPost, CommentOnTell, Post, Tell
from messagesapp.models import Message
from messagesapp.utils import returnChatsCountApi
from rest_framework import serializers
from users.models import Profile
from django.contrib.auth.models import User

# create your user serializers over here

class MessageSerializer(serializers.ModelSerializer):
   class Meta:
      model = Message
      fields = '__all__'
class ProfileSerializer(serializers.ModelSerializer):
   msgcount = serializers.SerializerMethodField()
   last_seen = serializers.SerializerMethodField()

   class Meta:
      model = Profile
      fields = '__all__'

   def get_last_seen(self, obj):
      return obj.get_last_seen

   def get_msgcount(self, obj):
      unread_msg = returnChatsCountApi(obj.user)
      print(f"unread_messages: {unread_msg}")
      return unread_msg


class UserSerializer(serializers.ModelSerializer):
   profile = serializers.SerializerMethodField()
   class Meta:
      model = User
      fields = '__all__'

   def get_profile(self, obj):
      profile = obj.profile
      serializer = ProfileSerializer(profile, many=False)
      return serializer.data





class CommentPostSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)

   class Meta:
      model = CommentOnPost
      fields = '__all__'
class PostSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)
   liked = serializers.SerializerMethodField("_liked")
   comments = serializers.SerializerMethodField()
   date = serializers.SerializerMethodField()
   # liked = serializers.SerializerMethodField()

   class Meta:
      model = Post
      fields = '__all__'

   def _liked(self, obj):
      user = self.context["request"].user # RECIEVING CONTEXT
      if user in obj.likers.all():
         return True
      else:
         return False

   def get_comments(self, obj):
      comments = obj.commentonpost_set.all()
      serializers = CommentPostSerializer(comments, many=True)
      return serializers.data

   def get_date(self, obj):
      date = obj.get_date
      return date



class CommentTellSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)

   class Meta:
      model = CommentOnTell
      fields = '__all__'

class TellOnTellSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)
   class Meta:
      model = Tell
      fields = '__all__'
class TellOnPostSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)
   class Meta:
      model = Post
      fields = '__all__'
class TellSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)
   tell_on_post = TellOnPostSerializer(many=False)
   tell_on_tell = TellOnTellSerializer(many=False)
   
   liked = serializers.SerializerMethodField("_liked")
   comments = serializers.SerializerMethodField()
   date = serializers.SerializerMethodField()

   class Meta:
      model = Tell
      fields = '__all__'

   def _liked(self, obj):
      user = self.context["request"].user # RECIEVING CONTEXT
      if user in obj.likers.all():
         return True
      else:
         return False

   def get_date(self, obj):
      date = obj.get_time
      return date

   def get_comments(self, obj):
      # Grab comments for Post if it's a tell on post Tell
      # Grab comments for Tell if it's a tell on tell Tell
      # Grab comments for the main tell. default
      # match (obj.type):
      #    case "post":
      #       comments = obj.tell_on_post.commentonpost_set.all()
      #       serializer = CommentPostSerializer(comments, many=True)
      #    case "tell":
      #       comments = obj.tell_on_tell.commentontell_set.all()
      #       serializer = CommentTellSerializer(comments, many=True)
      #    case default:
      #       comments = obj.commentontell_set.all()
      #       serializer = CommentTellSerializer(comments, many=True)
      comments = obj.commentontell_set.all()
      serializer = CommentTellSerializer(comments, many=True)
      return serializer.data
   owner = UserSerializer(many=False)
   liked = serializers.SerializerMethodField("_liked")
   comments = serializers.SerializerMethodField()
   date = serializers.SerializerMethodField()

   class Meta:
      model = Tell
      fields = '__all__'

   def _liked(self, obj):
      user = self.context["request"].user # RECIEVING CONTEXT
      if user in obj.likers.all():
         return True
      else:
         return False

   def get_date(self, obj):
      date = obj.get_time
      return date

   def get_comments(self, obj):
      comments = obj.commentontell_set.all()
      # print(f"Comments: {comments}")
      serializer = CommentTellSerializer(comments, many=True)
      return serializer.data

class Post2Serializer(serializers.ModelSerializer):
   class Meta:
      model = Post
      fields = "__all__"

class ProfileWithPostSerializer(serializers.ModelSerializer):
   posts = serializers.SerializerMethodField()

   class Meta:
      model = Profile
      fields = '__all__'

   def get_posts(self, obj):
      posts = obj.user.post_set.all()[:3]
      # print("POSTSSS: ", posts)
      serializer = Post2Serializer(posts, many=True)
      return serializer.data


class ActivitySerializer(serializers.ModelSerializer):
   profile = serializers.SerializerMethodField()
   post = Post2Serializer(many=False)
   comment = serializers.SerializerMethodField()
   date = serializers.SerializerMethodField()

   class Meta:
      model = Activity
      fields = '__all__'

   def get_profile(self, obj):
      profile = obj.user.profile
      serializer = ProfileSerializer(profile, many=False)
      return serializer.data

   def get_date(self, obj):
      return str(obj.get_time)

   # like_post, like_tell, comment_post, comment_tell, follow
   # def get_post(self, obj):
   #    if obj.activity_type == "like_post" or obj.activity_type == "comment_post":
   #       serializer = Post2Serializer(obj.post, many=False)
   #       return serializer.data
   #    else: return ""


   def get_comment(self, obj):
      if obj.activity_type == "comment_post":
         comment = obj.comment_post.comment
         # print('COMMENT: ', comment)
         return str(comment)
      elif obj.activity_type == "comment_tell":
         comment = obj.comment_tell.comment
         # print('COMMENT: ', comment)
         return str(comment)

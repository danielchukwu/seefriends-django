from email.policy import default
from urllib import request
from rest_framework import serializers
from homeapp.models import CommentOnPost, CommentOnTell, Post, Tell
from users.models import Profile
from django.contrib.auth.models import User



class ProfileSerializer(serializers.ModelSerializer):
   class Meta:
      model = Profile
      fields = '__all__'

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
   liked = serializers.SerializerMethodField("_liked")

   class Meta:
      model = Tell
      fields = '__all__'
   
   def _liked(self, obj):
      user = self.context["request"].user # RECIEVING CONTEXT
      if user in obj.likers.all():
         return True
      else:
         return False
class TellOnPostSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)
   liked = serializers.SerializerMethodField("_liked")

   def _liked(self, obj):
      user = self.context["request"].user # RECIEVING CONTEXT
      if user in obj.likers.all():
         return True
      else:
         return False

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
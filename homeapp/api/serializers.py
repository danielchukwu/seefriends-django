from email.policy import default
from urllib import request
from rest_framework import serializers
from homeapp.models import CommentOnPost, CommentOnTell, Post, Search, Tell
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


# Comment Serializers
class CommentPostSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)

   class Meta:
      model = CommentOnPost
      fields = '__all__'
class CommentTellSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)

   class Meta:
      model = CommentOnTell
      fields = '__all__'

# Tell on Serializers
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

# Post and Tell Serializers
class PostSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)
   liked = serializers.SerializerMethodField("_liked")
   comments = serializers.SerializerMethodField()
   date = serializers.SerializerMethodField()

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
      comments = obj.commentontell_set.all()
      serializer = CommentTellSerializer(comments, many=True)
      return serializer.data

# Post an Tell Single Serializers
class PostSingleSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)
   liked = serializers.SerializerMethodField("_liked")
   comments = serializers.SerializerMethodField()
   date = serializers.SerializerMethodField()
   threads = serializers.SerializerMethodField()

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

   def get_threads(self, obj):
      tells = obj.tell_set.all()
      serializer = TellSerializer(tells, many=True, context={'request': self.context["request"]})
      return serializer.data

class TellSingleSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)
   tell_on_post = TellOnPostSerializer(many=False)
   tell_on_tell = TellOnTellSerializer(many=False)  
   
   liked = serializers.SerializerMethodField("_liked")
   comments = serializers.SerializerMethodField()
   date = serializers.SerializerMethodField()
   threads = serializers.SerializerMethodField()

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
      serializer = CommentTellSerializer(comments, many=True)
      return serializer.data

   def get_threads(self, obj):
      tells = obj.tell_on_tell_now.all()
      serializer = TellSerializer(tells, many=True, context={'request': self.context["request"]})
      return serializer.data


# Search Serializer
class SearchSerializer(serializers.ModelSerializer):
   user = UserSerializer()
   class Meta:
      model = Search
      fields = '__all__'


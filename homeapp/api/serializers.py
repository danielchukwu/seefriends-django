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
   comments = serializers.SerializerMethodField()
   date = serializers.SerializerMethodField()

   class Meta:
      model = Post
      fields = '__all__'

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


class TellSerializer(serializers.ModelSerializer):
   owner = UserSerializer(many=False)
   comments = serializers.SerializerMethodField()

   class Meta:
      model = Tell
      fields = '__all__'

   def get_comments(self, obj):
      comments = obj.commentontell_set.all()
      # print(f"Comments: {comments}")
      serializer = CommentTellSerializer(comments, many=True)
      return serializer.data
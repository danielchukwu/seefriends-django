from homeapp.models import Activity, CommentOnPost, CommentOnTell, Post, Tell
from rest_framework import serializers
from users.models import Profile
from django.contrib.auth.models import User

# create your user serializers over here

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


class ActivitySerializer(serializers.ModelSerializer):
   profile = serializers.SerializerMethodField()
   postimg = serializers.SerializerMethodField()
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
   def get_postimg(self, obj):
      if obj.activity_type == "like_post" or obj.activity_type == "comment_post":
         img = obj.post.img
         return str(img)
      else: return ""


   def get_comment(self, obj):
      if obj.activity_type == "comment_post":
         comment = obj.comment_post.comment
         print('COMMENT: ', comment)
         return str(comment)
      elif obj.activity_type == "comment_tell":
         comment = obj.comment_tell.comment
         print('COMMENT: ', comment)
         return str(comment)



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
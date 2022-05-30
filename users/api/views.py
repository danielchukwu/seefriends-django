from .serializers import ActivitySerializer, PostSerializer, TellSerializer, UserSerializer
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.api import serializers

# create your user views here

@api_view(['GET'])
def getOwner(request):
   user = request.user
   serializer= UserSerializer(user, many=False)
   return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getUser(request, pk):
   user = User.objects.get(id=pk)
   serializer = UserSerializer(user, many=False)
   return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getActivities(request):
   if (request.user):
      profile = request.user.profile
      profile.activity_count = 0
      profile.save()
      print(f"Activity Count: {profile.activity_count}")
   activities = request.user.activity_set.all()
   # print(activities)
   serializer = ActivitySerializer(activities, many=True)
   return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserPost(request, pk):
   user = User.objects.get(id=pk)
   posts = user.post_set.all()
   serializer = PostSerializer(posts, many=True)
   return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserTells(request, pk):
   user = User.objects.get(id=pk)
   tells = user.tell_set.all()
   print("tells:", tells)
   serializer = TellSerializer(tells, many=True)
   return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSavedPosts(request):
   if (request.method == "GET"):
      saved_post = request.user.profile.saved_post.all()
      print(saved_post)
      serializer = PostSerializer(saved_post, many=True)
      # print("saved_post:", saved_post)
      return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSavedTells(request):
   saved_tell = request.user.profile.saved_tell.all()
   serializer = TellSerializer(saved_tell, many=True)
   print("saved_tell:", saved_tell)
   return Response(serializer.data)


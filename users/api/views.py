from .serializers import ActivitySerializer, PostSerializer, UserSerializer
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
   print("I AM HERE ............................................................")
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
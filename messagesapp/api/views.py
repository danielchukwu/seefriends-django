from multiprocessing import context
from users.models import UserFollower, UserFollowing
from .serializers import ActivitySerializer, PostSerializer, TellSerializer, UserSerializer
from homeapp.models import Activity, Post, PostFeed, Tell, SavePost, SaveTell

from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.api import serializers

# create your message views here


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fun(request):
   return Response([])
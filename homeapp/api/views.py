from homeapp.api.serializers import PostSerializer, TellSerializer, UserSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from homeapp.models import Post, Tell

# create your api views here

@api_view(['GET'])
def getRoutes(requet):
   routes = [
      {'GET': '/api/posts'},
      {'GET' : '/api/posts/:id'},
      {'PUT' : '/api/posts/:id'},
      {'POST' : '/api/posts'},

      {'POST' : '/api/users/token'},
      {'POST' : '/api/users/token/refresh'},
   ]

   return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPosts(request):
   print(request.user)

   posts = Post.objects.all()
   serializer = PostSerializer(posts, many=True)
   return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTells(request):
   tells = Tell.objects.all()
   serializer = TellSerializer(tells, many=True)
   return Response(serializer.data)
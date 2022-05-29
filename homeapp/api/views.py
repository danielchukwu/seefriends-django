from homeapp.api.serializers import PostSerializer, TellSerializer, UserSerializer
from homeapp.forms import PostForm

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


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def getPosts(request):
   if (request.method == "GET"):
      posts = Post.objects.all()
      serializer = PostSerializer(posts, many=True)
      return Response(serializer.data)

   elif (request.method == "POST"):
      Post.objects.create(
         owner = request.user,
         img = request.data['img'],
         body = request.data['body']
      )
      return Response({"message":"successful"})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def getTells(request):
   if (request.method == "GET"):
      tells = Tell.objects.all()
      serializer = TellSerializer(tells, many=True)
      return Response(serializer.data)
   elif (request.method == "POST"):
      Tell.objects.create(
         owner = request.user,
         body = request.data['body']
      )
      return Response({"message":"successful"})

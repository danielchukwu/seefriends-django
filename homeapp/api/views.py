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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getPosts(request):
   if (request.method == "GET"):
      print(request.user)

      posts = Post.objects.all()
      serializer = PostSerializer(posts, many=True)
      return Response(serializer.data)
   elif (request.method == "POST"):
      print("You Made It here!!!")
      user = request.user
      print(request.user)
      # form = PostForm(request.data, {'img': request.data['img']})
      # if form.is_valid:
      #    print("Form is Valid")
      #    print("request.data: ", )
      #    print("request.FILES:", request.FILES)
      #    # post = form.save(commit=False)
      #    # post.owner = user
      #    # print(post.owner)
      #    # post.save()
      print("request.data:",request.data)
      # post = Post.objects.create(
      #    owner = request.user,
      #    img = request.data['img'],
      #    body = request.data['body']
      # )
      # post.save()
      return Response(["Successful"])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTells(request):
   tells = Tell.objects.all()
   serializer = TellSerializer(tells, many=True)
   return Response(serializer.data)

# CRUD - Adding Post
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def addPost(request):
#    print("You Made It here!!!")
#    return Response([])
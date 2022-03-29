from ast import Return
from unicodedata import name
from django.urls import path
from . import views


# create your urls here

urlpatterns = [
   path('', views.home, name="home"),
   path('tells/', views.tellsPage, name="tells"),
   path('like-tell/<str:pk>/', views.likeTell, name="like-tell"),
   path('unlike-tell/<str:pk>/', views.unlikeTell, name="unlike-tell"),
   
   path('tell-form/', views.tellForm, name='tell-form'),
   path('tell-comments-page/<str:pk>/', views.tellCommentsPage, name="tell-comments-page"),
   path('add-tell-comment/<str:pk>/', views.addTellComment, name="add-tell-comment"),

   path('add-post-comment/<str:pk>/', views.addPostComment, name="add-post-comment"),
   path('post-comments-page/<str:pk>/', views.postCommentsPage, name="post-comments-page"),
   
   path('like-post/<str:pk>/', views.likePost, name="like-post"),
   path('unlike-post/<str:pk>/', views.unlikePost, name="unlike-post"),


   path('create-post/', views.createPost, name="create-post"),
]
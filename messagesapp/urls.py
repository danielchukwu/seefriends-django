from django.urls import path
from . import views

# create your urls here

urlpatterns = [
   path('', views.chat, name="chat"),
   path('message/<str:pk>/', views.message, name="message"),
   path('feed/', views.feed, name="feed"),
   path('friends/', views.friends, name="friends"),

   path('requests/', views.requests, name="requests"),
   path('request-message/<str:pk>/', views.requestMessage, name="request-message"),

   path('accept-request/<str:pk>/', views.acceptRequest, name="accept-request"),
]
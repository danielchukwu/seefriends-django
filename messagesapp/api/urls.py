from django.urls import path

from messagesapp.views import acceptRequest
from . import views

# create your urls here

urlpatterns = [
   path('', views.messages),
   path('requests/', views.requests),

   path('<str:pk>/', views.messageChat), # "GET": Gets chat with a user and "POST": sends body to that chat
   path('<str:pk>/remove/', views.exitRoom), # "GET": This goes to the room containing you and the other user and removes you from that room
   path('requests/<str:pk>/', views.requestsChat),
   
   path('requests/<str:pk>/accept/', views.acceptRequest)
]
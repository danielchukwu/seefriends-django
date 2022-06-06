from django.urls import path

from messagesapp.views import acceptRequest
from . import views

# create your urls here

urlpatterns = [
   path('', views.messages),
   path('requests/', views.requests),

   path('<str:pk>/', views.messageChat), # "GET": Gets chat with a user and "POST": sends body to that chat
   path('requests/<str:pk>/', views.requestsChat),
   
   path('requests/<str:pk>/accept/', views.acceptRequest)
]
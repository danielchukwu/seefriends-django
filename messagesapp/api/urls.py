from django.urls import path
from . import views

# create your urls here

urlpatterns = [
   path('', views.messages),
   path('<str:pk>/', views.messageChat), # "GET": Gets chat with a user and "POST": sends body to that chat
]
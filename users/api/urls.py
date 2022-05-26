from django.urls import path

from . import views
# create your api endpoints here

urlpatterns = [
   path('', views.getOwner),
   path('<str:pk>/', views.getUser),
   path('activity/', views.getActivities),
   path('<str:pk>/posts/', views.getUserPost),
]
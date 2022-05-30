from django.urls import path

from . import views
# create your api endpoints here

urlpatterns = [
   path('', views.getOwner),
   path('activity/', views.getActivities),
   path('saved-posts/', views.getSavedPosts),
   path('saved-tells/', views.getSavedTells),

   path('<str:pk>/', views.getUser),
   path('<str:pk>/posts/', views.getUserPost),
   path('<str:pk>/tells/', views.getUserTells),

   path('<str:pk>/followers/', views.getFollowers),
   path('<str:pk>/following/', views.getFollowings),
   path('<str:pk>/friends/', views.getFriends),
]
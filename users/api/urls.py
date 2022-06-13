from django.urls import path

from . import views
# create your api endpoints here

urlpatterns = [
   path('', views.getOwner),
   path('profiles/', views.getProfiles),

   path('update/', views.updateProfile),

   path('register/', views.registerUser),
   
   path('activity/', views.getActivities),
   path('saved-posts/', views.getSavedPosts),
   path('saved-tells/', views.getSavedTells),

   path('<str:pk>/', views.getUser),
   path('<str:pk>/posts/', views.getUserPost),
   path('<str:pk>/tells/', views.getUserTells),

   path('<str:pk>/followers/', views.getFollowers),
   path('<str:pk>/following/', views.getFollowings),
   path('<str:pk>/friends/', views.getFriends),

   path('<str:pk>/follow/', views.follow),
   path('<str:pk>/unfollow/', views.unfollow),
]
from django.urls import path
from . import views

# create your urls here

urlpatterns = [
   path('user-profile/', views.userProfile, name="user-profile"),
   path('user-profile-tells/', views.userProfileTells, name="user-profile-tells"),
   path('other-profile/<str:pk>/', views.otherProfile, name="other-profile"),
   path('other-profile-tells/<str:pk>/', views.otherProfileTells, name="other-profile-tells"),

   path('follow/<str:pk>/', views.follow, name="follow"),
   path('unfollow/<str:pk>/', views.unfollow, name="unfollow"),

   path('login/', views.loginUser, name="login"),
   path('logout/', views.logoutUser, name="logout"),
   path('sign-up/', views.registerUser, name="sign-up"),

   path('update-profile/', views.updateProfile, name="update-profile"),

   path('saved-post/', views.savedPostPage, name="saved-post-page"),
   path('save-post/<str:pk>/', views.savePost, name="save-post"),

   path('saved-tell/', views.savedTellPage, name="saved-tell-page"),
   path('save-tell/<str:pk>/', views.saveTell, name="save-tell"),
]
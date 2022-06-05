from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
   TokenObtainPairView,
   TokenRefreshView,
)

# create your api endpoints here

urlpatterns = [
   path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
   path('', views.getRoutes),
   path('posts/', views.getPosts),
   path('tells/', views.getTells),

   path('posts/<str:pk>/', views.getPost),
   path('tells/<str:pk>/', views.getTell),

   path('posts/<str:pk>/like/', views.likePost),
   path('tells/<str:pk>/like/', views.likeTell),

   path('posts/<str:pk>/comment/', views.commentOnPost),
   path('tells/<str:pk>/comment/', views.commentOnTell),

   path('posts/<str:pk>/save-post/', views.savePost),
   path('tells/<str:pk>/save-tell/', views.saveTell),

   path('posts/<str:pk>/tell-on-post/', views.tellOnPost),
   path('tells/<str:pk>/tell-on-tell/', views.tellOnTell),
   
   path('discover/', views.discover),
]
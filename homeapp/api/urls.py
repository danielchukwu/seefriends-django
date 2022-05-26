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
]
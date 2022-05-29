from django.urls import path

from . import views
# create your api endpoints here

urlpatterns = [
   path('', views.getOwner),
   path('activity/', views.getActivities),
   path('<str:pk>/', views.getUser),
   path('<str:pk>/posts/', views.getUserPost),
   path('<str:pk>/tells/', views.getUserTells),
]
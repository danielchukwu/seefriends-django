from django.urls import path
from . import views

# create your urls here

urlpatterns = [
   path('', views.messages),
]
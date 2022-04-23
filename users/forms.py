from django.forms.models import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

# create your forms here
class CustomUserCreationForm(UserCreationForm):
   class Meta:
      model = User
      fields = ['first_name', 'username', 'email', 'password1', 'password2']
      labels = {'first_name':'Full Name'}
         

class UpdateProfileForm(ModelForm):
   class Meta:
      model = Profile
      fields = ['name', 'username', 'email', 'img', 'bio']
      labels = {'name': 'full name'}


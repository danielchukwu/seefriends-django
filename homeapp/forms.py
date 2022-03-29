from django.forms.models import ModelForm
from .models import *

# create your forms here

class PostForm(ModelForm):
   class Meta:
      model = Post
      fields = ['img', 'body']
from django.contrib.auth.models import User

# create your utils here
def checkRegistration(username, email, password1, password2):
   form_errors = []

   if User.objects.filter(username__exact=username).count() > 0:
      print("username already exists")
      form_errors.append('username')
   if User.objects.filter(email__exact=email).count() > 0:
      print("email already exists")
      form_errors.append('email')
   if password1 != password2:
      print("passwords are not the same")
      form_errors.append('passwords unexact')
   if password1 == username or password1.lower().__contains__(username.lower()):
      print("password is equel to username")
      form_errors.append('password similar')
   if len(password1) < 8:
      print("password should b atleast 8 characters")
      form_errors.append('password short')

   return form_errors
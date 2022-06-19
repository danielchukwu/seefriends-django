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

def checkUpdate(request, username, email):
   form_errors = []

   if request.user.uprofile.username == username:
      # "no error since it's your username"
      pass
   elif User.objects.filter(username__exact=username).count() > 0:
      print("username already exists")
      form_errors.append('username')


   if request.user.uprofile.email == email:
      # "no error since it's your email"
      pass
   elif User.objects.filter(email__exact=email).count() > 0:
      print("email already exists")
      form_errors.append('email')

   valid_characters = 'a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9 _'
   valid_characters = valid_characters.split(' ')

   for char in username:
      if char.lower() in valid_characters:
         continue
      else:
         form_errors.append('not a username') # username contains unacceptable characters
         break


   return form_errors
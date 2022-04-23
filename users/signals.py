from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User

# create your signals here

from .models import Profile, Settings

# SECTION 1: Profile
def createProfile(sender, instance, created, **kwargs):
   # print(f"INSTANCE: {instance.first_name}")
   # print(f"INSTANCE: {created}")
   user = instance
   if created:
      profile = Profile.objects.create(
         user = user,
         name = user.first_name,
         username = user.username,
         email = user.email,
      )
post_save.connect(createProfile, sender=User)



# SECTION 2: User
def updateUser(sender, instance, created, **kwargs):
   if not created:
      user = instance.user
      profile = instance
      user.first_name = instance.name
      user.username = instance.username
      user.email = instance.email
      user.save()

post_save.connect(updateUser, sender=Profile)

# SECTION 3: create settings on user creation
def createSettings(sender, instance, created, **kwargs):
   user = instance
   if created:
      settings_creation = Settings.objects.create(owner = user)
post_save.connect(createSettings, sender=User)
from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import homeapp

class Profile(models.Model):
   VOTE_TYPE = (
      ('MALE', 'a male'),
      ('FEMALE', 'a female'),
   )
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   name = models.CharField(max_length=200, blank=True, null=True)
   username = models.CharField(max_length=200, blank=True, null=True, unique=True)
   email = models.EmailField(max_length=500, blank=True, null=True, unique=True)
   img = models.ImageField(upload_to="profiles/", default="icons/user.png")
   # gender = models.CharField(max_length=200, choices=VOTE_TYPE)
   bio = models.TextField(default="", blank=True, null=True)

   online = models.BooleanField(default=False)
   last_seen = models.DateTimeField(default=datetime.now(), null=True, blank=True)

   followers = models.ManyToManyField(User, related_name='followers', blank=True)
   following = models.ManyToManyField(User, related_name='following', blank=True)
   friends = models.ManyToManyField(User, related_name='friends', blank=True)
   verified = models.BooleanField(default=False)

   saved_post = models.ManyToManyField("homeapp.Post", related_name="saved_post", blank=True)
   saved_tell = models.ManyToManyField("homeapp.Tell", related_name="saved_tell", blank=True)
   
   seen_post = models.ManyToManyField("homeapp.Post", blank=True)
   seen_tell = models.ManyToManyField("homeapp.Tell", blank=True)

   activity_count = models.PositiveSmallIntegerField(default=0)
   # unread_msg_count = models.PositiveSmallIntegerField(default=0)

   updated = models.DateTimeField(auto_now_add=True)
   created = models.DateTimeField(auto_now=True)
   id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

   def __str__(self):
      return self.username
   
   @property
   def get_total_followers(self):
      return self.followers.count()
   
   @property
   def get_total_following(self):
      return self.following.count()

   @property
   def get_total_friends(self):
      return self.friends.count()

   def is_leapyear(self, year):
      # declared
      leap_year = None

      # process: calculate if input is a leap year
      if (year % 4 == 0):
         if (year % 100 == 0):           
            if (year % 400 == 0):
               leap_year = True
            else:
               leap_year = False
         else:
            leap_year = True
      else:
         leap_year = False

      return leap_year
   def returnDateInMinutesAgo(self, year, month, day, hour, minutes):
      is_a_leapyear = self.is_leapyear(year) # print(f"{year} is a leap year == {is_a_leapyear}")
      months_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
      months_days_leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

      days_for_months_ago = 0
      if is_a_leapyear == False: # print(f"Month: {month}")
         for index, days in enumerate(months_days):
            if index != month-1: # print(index+1, days)
               days_for_months_ago += days
            elif index == month-1: # print(f"stop month reached") #print(f"Total days: {days_for_months_ago + day}\n")
               break
      else:
         for index, days in enumerate(months_days_leap):
            if index != month-1: # print(index+1, days)
               days_for_months_ago += days
            elif index == month-1: # print(f"stop month reached") #print(f"Total days: {days_for_months_ago + day}\n")
               break
      total_days = (days_for_months_ago + day)

      total_minutes = minutes + (hour * 60) + ( (total_days * 24) * 60)
      return total_minutes

   def get_time(self, h, m):
      "we add + 1 to hour because django created time hour has a -1 bug or error. so to fix when displaying time to a user is we add 1 to the hour"
      
      if h + 1 < 10:
         hour = f"0{h + 1}"
      else:
         hour = f"{h + 1}"

      if m < 10:
         minutes = f"0{m}"
      else:
         minutes = f"{m}"

      return f"{hour}:{minutes}"

   @property
   def get_last_seen(self):
      date = datetime.now()
      ls_date = self.last_seen   # print(date) # print(ls_date)
      
      if self.online == False:
         if date.year == ls_date.year:
            minutes_ago = self.returnDateInMinutesAgo(date.year, date.month, date.day, date.hour, date.minute) - self.returnDateInMinutesAgo(date.year, ls_date.month, ls_date.day, ls_date.hour, ls_date.minute)
            if date.day == ls_date.day:
               if minutes_ago < 60:
                  return f"last seen {minutes_ago} {'minutes' if minutes_ago != 1 else 'minute'} ago"
               elif minutes_ago < 1440:
                  return f"last seen today {self.get_time(ls_date.hour, ls_date.minute)}"
            elif date.month == ls_date.month and date.day-1 == ls_date.day:
               return f"last seen yesterday {self.get_time(ls_date.hour, ls_date.minute)}"
            else:
               months = {
               "1": "January",
               "2": "February",
               "3": "March",
               "4": "April",
               "5": "May",
               "6": "June",
               "7": "July",
               "8": "August",
               "9": "September",
               "10": "October",
               "11": "November",
               "12": "December"
               }

               return f"last seen {months[str(ls_date.month-1)].lower()} {ls_date.day} at {self.get_time(ls_date.hour, ls_date.minute)}"
      else:
         return "online"

class UserFollower(models.Model):
   me = models.ForeignKey(User, on_delete=models.CASCADE)
   follower_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_by_user")

   updated = models.DateTimeField(auto_now_add=True)
   created = models.DateTimeField(auto_now=True)
   id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

   class Meta:
      unique_together = ['me', 'follower_to']
      ordering = ['-created']

   def __str__(self):
      return f"{self.me} followed to -> {self.follower_to}"

class UserFollowing(models.Model):
   me = models.ForeignKey(User, on_delete=models.CASCADE)
   following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_a_user")

   updated = models.DateTimeField(auto_now_add=True)
   created = models.DateTimeField(auto_now=True)
   id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

   class Meta:
      unique_together = ['me', 'following']
      ordering = ['-created']

   def __str__(self):
      return f"{self.me} following -> {self.following}"

class Settings(models.Model):
   owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
   # CHATS
   last_seen = models.BooleanField(default=True) # if False: you won't be able to see other users last_seen
   stories_privacy = models.CharField(max_length=20, default="Everyone", null=True) # options: Everyone, Followers, Following, Friends, Nobody(except works different with this)
   stories_privacy_except = models.ManyToManyField(User, related_name='story_privacy_except', blank=True)
   read_reciet = models.BooleanField(default=True)
   top_all = models.BooleanField(default=False)   # ✅
   top_unread = models.BooleanField(default=True)   # ✅
   dark_mode_chat = models.BooleanField(default=False)

   # ACCOUNT
   # -> privacy
   private_account = models.BooleanField(default=False)
   comments_privacy = models.CharField(max_length=20, default="Everyone", null=True) # options: Everyone, Followers, Following, Friends, Nobody(except works different with this)
   comments_privacy_except = models.ManyToManyField(User, related_name='comment_privacy_except', blank=True)
   dark_mode_account = models.BooleanField(default=False)
   
   # DEFAULTS
   updated = models.DateTimeField(auto_now_add=True)
   created = models.DateTimeField(auto_now=True)
   id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

   def __str__(self) -> str:
      return f"{self.owner} -> settings"
   
   class Meta:
      ordering = ['-created']
      verbose_name_plural = "Settings"

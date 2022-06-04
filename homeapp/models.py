import math
import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from users.models import *

from datetime import datetime, timedelta

# 1. POST
# post
class Post(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   img = models.ImageField(upload_to='contents/', null=True, blank=True)
   body = models.TextField()
   likers = models.ManyToManyField(User, 'post_likers', blank=True)
   commenters = models.ManyToManyField(User, 'post_commenters', blank=True)
   saved_count = models.PositiveSmallIntegerField(default=0)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

   class Meta:
      ordering = ['-created']

   @property
   def get_total_likes(self):
      return self.likers.count()

   @property
   def get_date(self):
      date = datetime.now()
      # print(self.body)
      # print(self.created.hour)
      # print(date.hour)
      if date.month == self.created.month:
         if date.day == self.created.day:
            "+1 to all hours because of django hour -1 error"
            if date.hour == self.created.hour+1:
               if date.minute == self.created.minute:
                  return str(date.minute - self.created.minute) + " seconds ago"
               else:
                  return str(date.minute - self.created.minute) + " minutes ago"
            else:
               print(f"We Here {date.hour - self.created.hour}")
               return str(date.hour - self.created.hour) + " hours ago"
         return str(date.day - self.created.day) + " days ago"
      elif date.year == self.created.year:
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
         return str(months[str(self.created.month)]) + " " + str(self.created.day)
      else:
         return str(date.year - self.created.year) + " years ago"


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

   @property
   def is_feed_ready(self):
      "logic: Returns true or false if post was created within 2 days ago"
      max_days = 10    # days_ago handler: 
      date = datetime.now()
      postdate = self.created   # print(date) # print(postdate)

      if date.year == postdate.year:
         minutes_ago = self.returnDateInMinutesAgo(date.year, date.month, date.day, date.hour, date.minute) - self.returnDateInMinutesAgo(date.year, postdate.month, postdate.day, postdate.hour, postdate.minute) # print(f"Minutes Ago: {minutes_ago}")
         days_ago = minutes_ago / 1440 # print(f"Days Ago: {math.floor(days_ago)} \n")
         if days_ago < max_days:
            return True
         else:
            return False
      else: return False

   @property
   def get_time(self):
      date = datetime.now()
      cr_date = self.created   # print(date) # print(cr_date)

      if date.year == cr_date.year:
         minutes_ago = self.returnDateInMinutesAgo(date.year, date.month, date.day, date.hour, date.minute) - self.returnDateInMinutesAgo(date.year, cr_date.month, cr_date.day, cr_date.hour+1, cr_date.minute)
         if date.day == cr_date.day:
            print(minutes_ago)
            if minutes_ago < 60:
               return f"{minutes_ago} {'minutes' if minutes_ago != 1 else 'minute'} ago"
            elif minutes_ago < 1440:
               hour = minutes_ago // 60
               return f"{hour} {'hours' if hour != 1 else 'hour'} ago"
         elif date.month == cr_date.month and date.day-1 == cr_date.day:
            return f"yesterday"
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

            return f"{months[str(cr_date.month-1)][:3]} {cr_date.day}"

   def __str__(self):
      return str(self.owner) + " post - " + str(self.body[:30])

class PostFeed(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   post_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="p_owner")
   post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
   
   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

   class Meta:
      ordering = ['-created']
      verbose_name_plural = "PostFeed"

   def __str__(self) -> str:
      return f"{self.owner}.. Feed -> {self.post.body}"

# post comment
class CommentOnPost(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   post = models.ForeignKey(Post, on_delete=models.CASCADE)
   comment = models.CharField(max_length=2000)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
   
   class Meta:
      ordering = ['-created', '-updated']

   def __str__(self):
      return str(self.owner) + " commented - " + str(self.comment)


class Search(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="search_user")

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
   
   def __str__(self):
      return f"{self.owner} searched -> {self.user}"
   
   class Meta:
      ordering = ['-updated']
      verbose_name_plural = "Search"

# 2. TELL
# tell
class Tell(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   body = models.TextField()
   likers = models.ManyToManyField(User, 'likers', blank=True)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

   class Meta:
      ordering = ['-created', '-updated']

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

   

   @property
   def get_time(self):
      date = datetime.now()
      cr_date = self.created   # print(date) # print(cr_date)

      if date.year == cr_date.year:
         minutes_ago = self.returnDateInMinutesAgo(date.year, date.month, date.day, date.hour, date.minute) - self.returnDateInMinutesAgo(date.year, cr_date.month, cr_date.day, cr_date.hour+1, cr_date.minute)
         if date.day == cr_date.day:
            print(minutes_ago)
            if minutes_ago < 60:
               return f"{minutes_ago} {'minutes' if minutes_ago != 1 else 'minute'} ago"
            elif minutes_ago < 1440:
               hour = minutes_ago // 60
               return f"{hour} {'hours' if hour != 1 else 'hour'} ago"
         elif date.month == cr_date.month and date.day-1 == cr_date.day:
            return f"yesterday"
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

            return f"{months[str(cr_date.month-1)][:3]} {cr_date.day}"

   @property
   def get_total_likes(self):
      return self.likers.count()

   def __str__(self) -> str:
      return f"{str(self.owner)} tell - {str(self.body)}"

# tell comment
class CommentOnTell(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   tell = models.ForeignKey(Tell, on_delete=models.CASCADE)
   comment = models.CharField(max_length=200)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
   
   class Meta:
      ordering = ['-created', '-updated']

   def __str__(self):
      return str(self.owner) + " commented - " + str(self.comment)



# SECTION 2: SAVE POST & TELL
class SavePost(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
   
   updated = models.DateTimeField(auto_now_add=True)
   created = models.DateTimeField(auto_now=True)
   id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

   class Meta:
      unique_together = ['owner', 'post']

   def __str__(self):
      return str(self.post)

class SaveTell(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   tell = models.ForeignKey(Tell, on_delete=models.CASCADE, null=True)
   
   updated = models.DateTimeField(auto_now_add=True)
   created = models.DateTimeField(auto_now=True)
   id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

   class Meta:
      unique_together = ['owner', 'tell']

   def __str__(self):
      return str(self.tell)



# SECTION 3: ACTIVITY
class Activity(models.Model):
   owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True)
   activity_type = models.CharField(max_length=200, null=True, blank=True) # like_post, like_tell, comment_post, comment_tell, follow, new: friends

   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post", null=True)
   tell = models.ForeignKey(Tell, on_delete=models.CASCADE, related_name="tell", null=True)

   liker_post = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_liker", null=True)
   liker_tell = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tell_liker", null=True)
   comment_post = models.ForeignKey(CommentOnPost, on_delete=models.CASCADE, related_name="post_comment", null=True)
   comment_tell = models.ForeignKey(CommentOnTell, on_delete=models.CASCADE, related_name="tell_comment", null=True)

   updated = models.DateTimeField(auto_now_add=True)
   created = models.DateTimeField(auto_now=True)
   id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

   class Meta:
      ordering = ['-created']

   def __str__(self):
      return str(f"{self.owner} - {self.activity_type} activity from -> {self.user}")

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

   @property
   def get_time(self):
      date = datetime.now()
      cr_date = self.created   # print(date) # print(cr_date)

      if date.year == cr_date.year:
         minutes_ago = self.returnDateInMinutesAgo(date.year, date.month, date.day, date.hour, date.minute) - self.returnDateInMinutesAgo(date.year, cr_date.month, cr_date.day, cr_date.hour+1, cr_date.minute)
         if date.day == cr_date.day:
            print(minutes_ago)
            if minutes_ago < 60:
               return f"{minutes_ago} {'minutes' if minutes_ago != 1 else 'minute'} ago"
            elif minutes_ago < 1440:
               hour = minutes_ago // 60
               return f"{hour} {'hours' if hour != 1 else 'hour'} ago"
         elif date.month == cr_date.month and date.day-1 == cr_date.day:
            return f"yesterday"
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

            return f"{months[str(cr_date.month-1)][:3]} {cr_date.day}"


from datetime import datetime
from email.policy import default
from pickle import TRUE
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.

class Message(models.Model):
   owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
   recipient = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="messages", null=True, blank=True)

   request_accepted = models.BooleanField(default=False)

   unread_messages = models.IntegerField(default=0) # message: msg.2
   last_body = models.ForeignKey("Body", on_delete=models.SET_NULL, null=True, blank=True, related_name="last_body", default="") # message: msg.3
   subdate = models.DateTimeField(null=True, blank=True)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

   def __str__(self) -> str:
      return f"{self.owner} to -> {self.recipient}"

   class Meta:
      ordering = ['-updated']            # logic: so it appears in chats in the order of most recently updated
      unique_together = ['owner', 'recipient']

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
   def returnDaysAgo(self, year, month, day):
      is_a_leapyear = self.is_leapyear(year) # print(f"{year} is a leap year == {is_a_leapyear}")
      months_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
      months_days_leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

      days = 0

      days_for_months_ago = 0
      if is_a_leapyear == False: # print(f"Month: {month}")
         year_count = int(datetime.now().year - year) + 1
         while(year_count > 0):
            "use normal year months_days"
            if year_count == 1:
               "if this is current year? only add months days up on to our current month and stop"
               current_month = datetime.now().month
               days += sum(months_days[month-1 : current_month-1]) # -1 because the list index starts at 0
               days += datetime.now().day # we ought to -days from this. because we add the month of msg creation with no regard to the days offset 
               days -= day # let's just subtract the day of months post from total days
               year_count -= 1
            else:
               "if this is not current year? add all the days together"
               days += sum(months_days)
               year_count -= 1
      else:
         # "use leap year months_days instead"
         if year_count == 1:
            "if this is current year? only add months days up on to our current month and stop"
            current_month = datetime.now().month
            days += sum(months_days[month-1 : current_month-1]) # -1 because the list index starts at 0
            days += datetime.now().day # we ought to -days from this. because we add the month of msg creation with no regard to the days offset 
            days -= day # let's just subtract the day of months post from total days
            year_count -= 1
         else:
            "if this is not current year? add all the days together"
            days += sum(months_days_leap)
            year_count -= 1
      
      return days

   @property
   def get_time(self):
      date = datetime.now()
      cr_date = self.subdate   # print(date) # print(cr_date)

      if date.year == cr_date.year:
         if date.month == cr_date.month:
            if date.day == cr_date.day:
               hour = cr_date.hour+1 if cr_date.hour+1 >= 10 else f"0{cr_date.hour+1}"  # e.g hrs=> 10:-- or 05:--
               minutes = cr_date.minute if cr_date.minute >= 10 else f"0{cr_date.minute}" # e.g mins => --:34 or --:03
               return f"{hour}:{minutes}"
            else:
               days = date.day - cr_date.day
               if (days < 7):
                  return f"{days}d"
               else:
                  weeks = days // 7
                  return f"{weeks}w"
         else:
            days = self.returnDaysAgo(cr_date.year, cr_date.month, cr_date.day)
            return f"{days//7}w"
      else:
         days = self.returnDaysAgo(cr_date.year, cr_date.month, cr_date.day)
         return f"{days//7}w"



class Body(models.Model):
   owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
   recipient = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="body_recipient", null=True, blank=True)

   message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
   body = models.TextField()
   is_read = models.BooleanField(default=False)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

   def __str__(self) -> str:
      return f"Body -> {self.body[:50]}"

   @property
   def get_body_count(self):
      return len(self.body)

   @property
   def get_time(self):
      "we add + 1 to hour because django created time hour has a -1 bug or error. so to fix when displaying time to a user is we add 1 to the hour"
      hour = None
      minutes = None
      if self.created.hour + 1 < 10:
         hour = f"0{self.created.hour + 1}"
      else:
         hour = f"{self.created.hour + 1}"

      if self.created.minute < 10:
         minutes = f"0{self.created.minute}"
      else:
         minutes = f"{self.created.minute}"

      return f"{hour}:{minutes}"


   class Meta:
      verbose_name_plural = "Body"
      ordering = ['-created']

# purpose: for chatting in real-time
class Room(models.Model):
   room_name = models.CharField(max_length=50)
   participants = models.ManyToManyField(User, blank=True)

   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

   def __str__(self) -> str:
      return f"{self.room_name} room"

   @property
   def get_user_count(self):
      return self.participants.count()

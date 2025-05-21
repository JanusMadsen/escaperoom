from django.db import models

# Create your models here.

class RoomState(models.Model):
    door_open = models.BooleanField(default=False)
    lock_code = models.CharField(max_length=16, default="1234")  # Set your desired code length and default
    user_input = models.CharField(max_length=16, blank=True, default="")

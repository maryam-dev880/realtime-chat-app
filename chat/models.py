from django.db import models

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=100)

    def __str__(self):
        return self.room_name

class Message(models.Model):
    sender_name = models.TextField(max_length=15)
    message_detail = models.TextField(max_length=5000)
    created_time = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.message_detail
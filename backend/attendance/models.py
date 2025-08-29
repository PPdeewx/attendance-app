from django.db import models
from django.contrib.auth.models import User
import pickle

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class AttendanceLog(models.Model):
    TIME_CHOICES = [
        ('morning','เช้า'),
        ('noon','กลางวัน'),
        ('afternoon','บ่าย'),
        ('evening','เย็น')
    ]
    ACTION_CHOICES = [
        ('in', 'เข้า'),
        ('out', 'ออก'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    time_type = models.CharField(max_length=10, choices=TIME_CHOICES)
    action = models.CharField(max_length=3, choices=ACTION_CHOICES, default='in')
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    face_verified = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} {self.time_type} {self.action} @ {self.timestamp}"

class FaceProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face_encoding = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Face profile of {self.user.username}"
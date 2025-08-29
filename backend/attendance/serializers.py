from rest_framework import serializers
from .models import AttendanceLog, Location, FaceProfile

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'latitude', 'longitude']

class AttendanceLogSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

    class Meta:
        model = AttendanceLog
        fields = ['id', 'timestamp', 'time_type', 'location', 'action', 'user']

class FaceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceProfile
        fields = ['id', 'user', 'face_encoding', 'created_at']
        extra_kwargs = {
            'face_encoding': {'write_only': True}
        }
from django.contrib import admin
from .models import Location, AttendanceLog, FaceProfile

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'latitude', 'longitude')
    search_fields = ('name',)

@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'time_type', 'action', 'timestamp', 'location')
    list_filter = ('time_type', 'action', 'location')
    search_fields = ('user__username', 'location__name')

@admin.register(FaceProfile)
class FaceProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)
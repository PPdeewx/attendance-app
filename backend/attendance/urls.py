from django.urls import path
from .views import AttendanceCheckIn, LocationList, FaceRegister, FaceCheckIn
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('check-in/', AttendanceCheckIn.as_view()),
    path('locations/', LocationList.as_view()),
    path('face-register/', FaceRegister.as_view()),
    path('face-checkin/', FaceCheckIn.as_view()),
    path('login/', obtain_auth_token),
]

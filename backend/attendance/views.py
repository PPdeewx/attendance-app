import face_recognition
import pickle

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AttendanceLog, Location, FaceProfile
from .serializers import AttendanceLogSerializer, LocationSerializer
from math import radians, cos, sin, asin, sqrt


def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians,[lat1, lon1, lat2, lon2])
    dlat = lat2-lat1
    dlon = lon2-lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2*asin(sqrt(a))
    km = 6371*c
    return km*1000

class AttendanceCheckIn(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = AttendanceLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AttendanceLog.objects.filter(user=self.request.user).order_by('-timestamp')

    def post(self, request, *args, **kwargs):
        user = request.user
        location_id = request.data.get('location')
        time_type = request.data.get('time_type')
        action = request.data.get('action', 'in')
        try:
            latitude = float(request.data.get('latitude'))
            longitude = float(request.data.get('longitude'))
        except (TypeError, ValueError):
            return Response({"error":"Invalid coordinates"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response({"error":"Location not found"}, status=status.HTTP_404_NOT_FOUND)

        if haversine(latitude, longitude, location.latitude, location.longitude) > 200:
            return Response({"error":"You are too far from location ( > 200 m )"}, status=status.HTTP_400_BAD_REQUEST)

        face_verified = bool(request.data.get('face_verified', True))

        log = AttendanceLog.objects.create(
            user=user,
            location=location,
            time_type=time_type,
            action=action,
            latitude=latitude,
            longitude=longitude,
            face_verified=face_verified
        )
        return Response(AttendanceLogSerializer(log).data, status=status.HTTP_201_CREATED)

class LocationList(generics.ListAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    permission_classes = [IsAuthenticated]

class FaceRegister(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("image")
        if not file:
            return Response({"error": "No image uploaded"}, status=400)

        img = face_recognition.load_image_file(file)
        encodings = face_recognition.face_encodings(img)

        if not encodings:
            return Response({"error": "No face detected"}, status=400)

        encoding = pickle.dumps(encodings[0])
        FaceProfile.objects.update_or_create(
            user=request.user,
            defaults={"face_encoding": encoding}
        )

        return Response({"status": "Face registered successfully"})


class FaceCheckIn(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("image")
        if not file:
            return Response({"error": "No image uploaded"}, status=400)

        img = face_recognition.load_image_file(file)
        encodings = face_recognition.face_encodings(img)

        if not encodings:
            return Response({"error": "No face detected"}, status=400)

        encoding = encodings[0]

        try:
            profile = FaceProfile.objects.get(user=request.user)
        except FaceProfile.DoesNotExist:
            return Response({"error": "No face registered"}, status=404)

        known_encoding = pickle.loads(profile.face_encoding)
        match = face_recognition.compare_faces([known_encoding], encoding)

        if match[0]:
            return Response({"status": "Face recognized ✅"})
        return Response({"error": "Face mismatch ❌"}, status=403)
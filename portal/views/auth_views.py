from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from decouple import config
from portal.models import PortalUser
from portal.serializers import PortalUserSerializer

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"message": "Email and password are required", "code": 401}, status=status.HTTP_401_UNAUTHORIZED)

        user = PortalUser.objects.filter(email=email).first()

        if user and check_password(password, user.password_hash):
            if not user.is_active:
                return Response({"message": "Account deactivated", "code": 401}, status=status.HTTP_401_UNAUTHORIZED)
            
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

            return Response({
                "api_key": config('API_KEY', default=''),
                "user": {
                    "sf_user_id": user.sf_user_id,
                    "email": user.email,
                    "is_active": user.is_active
                },
                "message": "Login successful"
            }, status=status.HTTP_200_OK)
        
        return Response({"message": "Invalid credentials", "code": 401}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class MeView(APIView):
    def get(self, request):
        sf_user_id = request.headers.get('X-SF-User-Id') or request.GET.get('sf_user_id')
        user = None
        if sf_user_id:
             user = PortalUser.objects.filter(sf_user_id=sf_user_id).first()
        if not user:
             user = PortalUser.objects.filter(is_active=True).first()
             
        if not user:
             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
             
        serializer = PortalUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

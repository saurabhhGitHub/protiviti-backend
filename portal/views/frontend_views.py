from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({
            "status": "ok",
            "database": "connected",
            "timestamp": timezone.now().isoformat()
        })

class LoginPageView(TemplateView):
    template_name = 'portal/login.html'

class DashboardPageView(TemplateView):
    template_name = 'portal/dashboard.html'

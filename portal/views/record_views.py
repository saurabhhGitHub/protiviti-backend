import threading
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from portal.models import PortalRecord, PortalUser
from portal.serializers import PortalRecordSerializer
from decouple import config

def check_api_key(request):
    api_key_header = request.headers.get('X-API-Key')
    if not api_key_header or api_key_header != config('API_KEY', default=''):
        return False
    return True

def attempt_sf_sync(record_id):
    """
    Simulates a background MuleSoft / Salesforce write.
    """
    time.sleep(1)
    print(f"Simulating SF write for record {record_id}")
    
    try:
        record = PortalRecord.objects.get(id=record_id)
        record.sync_status = 'synced'
        record.save(update_fields=['sync_status'])
    except PortalRecord.DoesNotExist:
        pass

class RecordListCreateView(APIView):
    def get(self, request):
        if not check_api_key(request):
            return Response({"code": 401, "message": "Invalid or missing API Key"}, status=status.HTTP_401_UNAUTHORIZED)
            
        sf_user_id = request.headers.get('X-SF-User-Id')
        user = PortalUser.objects.filter(sf_user_id=sf_user_id).first()
        if not user:
            return Response({"error": "Valid X-SF-User-Id header required"}, status=status.HTTP_400_BAD_REQUEST)
            
        records = PortalRecord.objects.filter(owner=user)
        serializer = PortalRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not check_api_key(request):
            return Response({"code": 401, "message": "Invalid or missing API Key"}, status=status.HTTP_401_UNAUTHORIZED)
            
        sf_user_id = request.headers.get('X-SF-User-Id')
        user = PortalUser.objects.filter(sf_user_id=sf_user_id).first()
        if not user:
            return Response({"error": "Valid X-SF-User-Id header required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PortalRecordSerializer(data=request.data)
        if serializer.is_valid():
            record = serializer.save(owner=user, sync_status='pending')
            threading.Thread(target=attempt_sf_sync, args=(record.id,)).start()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecordDetailView(APIView):
    def get_object(self, pk, user):
        return get_object_or_404(PortalRecord, pk=pk, owner=user)

    def get(self, request, pk):
        if not check_api_key(request):
            return Response({"code": 401, "message": "Invalid or missing API Key"}, status=status.HTTP_401_UNAUTHORIZED)
            
        sf_user_id = request.headers.get('X-SF-User-Id')
        user = PortalUser.objects.filter(sf_user_id=sf_user_id).first()
        if not user:
            return Response({"error": "Valid X-SF-User-Id header required"}, status=status.HTTP_400_BAD_REQUEST)

        record = self.get_object(pk, user)
        serializer = PortalRecordSerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not check_api_key(request):
            return Response({"code": 401, "message": "Invalid or missing API Key"}, status=status.HTTP_401_UNAUTHORIZED)
            
        sf_user_id = request.headers.get('X-SF-User-Id')
        user = PortalUser.objects.filter(sf_user_id=sf_user_id).first()
        if not user:
            return Response({"error": "Valid X-SF-User-Id header required"}, status=status.HTTP_400_BAD_REQUEST)

        record = self.get_object(pk, user)
        serializer = PortalRecordSerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            record = serializer.save(sync_status='pending')
            threading.Thread(target=attempt_sf_sync, args=(record.id,)).start()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

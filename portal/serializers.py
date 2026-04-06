from rest_framework import serializers
from portal.models import PortalUser, PortalRecord

class PortalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortalUser
        exclude = ('password_hash',)

class PortalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortalRecord
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'sync_status', 'sf_record_id', 'created_at', 'updated_at')

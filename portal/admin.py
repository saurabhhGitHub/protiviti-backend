from django.contrib import admin
from portal.models import PortalUser, PortalRecord

@admin.register(PortalUser)
class PortalUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'sf_user_id', 'is_active', 'sync_status', 'last_login')

@admin.register(PortalRecord)
class PortalRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'sync_status', 'created_at')

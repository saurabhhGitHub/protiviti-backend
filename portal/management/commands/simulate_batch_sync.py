from django.core.management.base import BaseCommand
from portal.models import PortalRecord

class Command(BaseCommand):
    help = 'Simulates MuleSoft daily batch job'

    def handle(self, *args, **kwargs):
        records = PortalRecord.objects.filter(sync_status='pending')
        count = records.count()
        
        for record in records:
            self.stdout.write(f"Syncing record {record.id}...")
            record.sync_status = 'synced'
            record.save(update_fields=['sync_status'])
            
        self.stdout.write(self.style.SUCCESS(f"Batch sync complete. {count} records synced."))

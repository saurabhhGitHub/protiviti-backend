from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from portal.models import PortalUser

class Command(BaseCommand):
    help = 'Seeds 3 demo users for Portal login testing simulating sync state'

    def handle(self, *args, **kwargs):
        users_data = [
            {'email': 'admin@protiviti.com', 'password': 'Admin@123', 'sf_user_id': 'SF001'},
            {'email': 'jane@protiviti.com', 'password': 'Jane@123', 'sf_user_id': 'SF002'},
            {'email': 'john@protiviti.com', 'password': 'John@123', 'sf_user_id': 'SF003'},
        ]

        for data in users_data:
            PortalUser.objects.update_or_create(
                email=data['email'],
                defaults={
                    'password_hash': make_password(data['password'], hasher='bcrypt'),
                    'sf_user_id': data['sf_user_id'],
                    'is_active': True,
                    'sync_status': 'synced'
                }
            )

        self.stdout.write(self.style.SUCCESS("Seeded 3 demo users"))

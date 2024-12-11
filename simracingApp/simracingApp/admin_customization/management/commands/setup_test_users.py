from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test users for different admin roles'

    def handle(self, *args, **options):
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write('Created superuser')

        # Create full admin user
        full_admin, created = User.objects.get_or_create(
            username='fulladmin',
            defaults={
                'email': 'fulladmin@example.com',
                'is_staff': True
            }
        )
        if created:
            full_admin.set_password('fulladmin')
            full_admin.save()
            full_admin_group = Group.objects.get(name='Full Admin')
            full_admin.groups.add(full_admin_group)
            self.stdout.write('Created full admin user')

        # Create limited admin user
        limited_admin, created = User.objects.get_or_create(
            username='limitedadmin',
            defaults={
                'email': 'limitedadmin@example.com',
                'is_staff': True
            }
        )
        if created:
            limited_admin.set_password('limitedadmin')
            limited_admin.save()
            limited_admin_group = Group.objects.get(name='Limited Admin')
            limited_admin.groups.add(limited_admin_group)
            self.stdout.write('Created limited admin user') 
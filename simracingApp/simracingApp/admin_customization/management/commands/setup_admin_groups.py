from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from simracingApp.posts.models import Post
from simracingApp.events.models import Event

class Command(BaseCommand):
    help = 'Creates admin groups with specific permissions'

    def handle(self, *args, **options):
        # Create Full Admin group
        full_admin_group, created = Group.objects.get_or_create(name='Full Admin')
        if created:
            self.stdout.write('Created Full Admin group')

        # Create Limited Admin group
        limited_admin_group, created = Group.objects.get_or_create(name='Limited Admin')
        if created:
            self.stdout.write('Created Limited Admin group')

        # Get content types
        post_content_type = ContentType.objects.get_for_model(Post)
        event_content_type = ContentType.objects.get_for_model(Event)

        # Define permissions for Full Admins (all permissions)
        full_admin_permissions = Permission.objects.filter(
            content_type__in=[post_content_type, event_content_type]
        )
        full_admin_group.permissions.set(full_admin_permissions)

        # Define permissions for Limited Admins (only view and change)
        limited_admin_permissions = Permission.objects.filter(
            content_type__in=[post_content_type, event_content_type],
            codename__in=['view_post', 'change_post', 'view_event', 'change_event']
        )
        limited_admin_group.permissions.set(limited_admin_permissions)

        self.stdout.write(self.style.SUCCESS('Successfully set up admin groups')) 
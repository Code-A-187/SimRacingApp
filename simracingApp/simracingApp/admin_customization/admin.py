from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from simracingApp.posts.models import Post
from simracingApp.events.models import Event

class CustomAdminSite(admin.AdminSite):
    site_header = 'SimRacing Administration'
    site_title = 'SimRacing Admin Portal'
    index_title = 'Admin Management'

    def has_permission(self, request):
        """
        Check if user is superuser or belongs to admin groups
        """
        return (
            request.user.is_active and 
            (request.user.is_superuser or 
             request.user.groups.filter(name__in=['Full Admin', 'Limited Admin']).exists())
        )

admin_site = CustomAdminSite(name='custom_admin')

# Register models with custom ModelAdmin classes
class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Limited admins can only see non-superuser users
            qs = qs.filter(is_superuser=False)
        return qs

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='Full Admin').exists():
            if obj and obj.is_superuser:
                return False
            return True
        return False

# Register models
admin_site.register(User, CustomUserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(Post)
admin_site.register(Event)

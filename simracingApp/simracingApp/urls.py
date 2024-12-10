from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from simracingApp import common

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('simracingApp.common.urls')),
    path('accounts/', include('simracingApp.accounts.urls')),
    path('posts/', include('simracingApp.posts.urls')),
    path('events/', include('simracingApp.events.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

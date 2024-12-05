from django.contrib import admin
from django.urls import path, include

from simracingApp import common

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('simracingApp.common.urls')),
    path('accounts/', include('simracingApp.accounts.urls')),
]

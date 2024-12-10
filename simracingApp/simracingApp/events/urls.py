from django.urls import path
from django.urls import include
from .views import (
    EventListView,
    EventDetailsView,
    EventCreateView,
    EventEditView,
    EventDeleteView,
    toggle_subscribe,
)

urlpatterns = (
    path('', EventListView.as_view(), name='event-list'),
    path('add/', EventCreateView.as_view(), name='event-add'),
    path('<int:pk>/', include([
        path('', EventDetailsView.as_view(), name='event-details'),
        path('edit/', EventEditView.as_view(), name='event-edit'),
        path('delete/', EventDeleteView.as_view(), name='event-delete'),
        path('subscribe/', toggle_subscribe, name='toggle-subscribe'),
    ])),
) 
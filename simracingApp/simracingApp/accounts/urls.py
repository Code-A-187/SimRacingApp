from django.urls import path
from django.contrib.messages.views import SuccessMessageMixin

from simracingApp.accounts import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register-page'),
    path('login/', views.UserLoginView.as_view(), name='login-page'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.ProfileDetailsView.as_view(), name='profile-details'),
]
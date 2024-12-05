from django.urls import path, include
from simracingApp.accounts import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register-page'),
    path('login/', views.UserLoginView.as_view(), name='login-page'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<int:pk>/', include([
        path('', views.ProfileDetailsView.as_view(), name='profile-details'),
        path('edit/', views.ProfileEditView.as_view(), name='profile-edit'),
        # path('delete/', views.ProfileDeleteView.as_view(), name='profile-delete'),
    ])),
]
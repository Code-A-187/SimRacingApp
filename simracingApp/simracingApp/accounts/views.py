from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib import messages

from simracingApp.accounts.forms import UserCreationForm, UserAuthenticationForm

UserModel = get_user_model()


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        response = super().form_valid(form)  # This saves the user
        # Now we can log in the user
        login(self.request, self.object)  # self.object is set by CreateView after save
        return response

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home-page')
        return super().get(request, *args, **kwargs)


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'accounts/login-page.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home-page')

    def get_success_url(self):
        return self.success_url


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home-page')


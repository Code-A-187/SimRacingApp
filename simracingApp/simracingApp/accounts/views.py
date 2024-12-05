from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from simracingApp.accounts.forms import UserAuthenticationForm, ProfileEditForm, UserRegisterForm

UserModel = get_user_model()


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
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
        return get_object_or_404(UserModel, pk=self.kwargs['pk'])


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home-page')


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'
    success_url = reverse_lazy('profile-details')

    def test_func(self):
        profile = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.object.pk
            }
        )


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete.html'
    success_url = reverse_lazy('home-page')
    
    def test_func(self):
        # Only allow users to delete their own profile
        profile = self.get_object()
        return self.request.user == profile

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your profile has been successfully deleted.')
        logout(request)  # Log out the user after deletion
        return super().delete(request, *args, **kwargs)

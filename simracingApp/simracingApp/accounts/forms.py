from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from simracingApp.accounts.models import User

UserModel = get_user_model()


class UserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        # Add placeholders
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your username'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Enter your password'
        })


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes and placeholders
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'avatar', 'bio', 'role']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your username'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your email'
                }
            ),
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Tell us about yourself',
                    'rows': 4
                }
            ),
            'role': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'avatar': forms.FileInput(
                attrs={
                    'class': 'form-control-file'
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserModel.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('Email is already in use.')
        return email

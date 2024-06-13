from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.',
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': 'input-field'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.',
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'class': 'input-field'
        })
    )
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'input-field'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'input-field'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Password',
                'class': 'input-field'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirm Password',
                'class': 'input-field'
            }),
        }

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'input-field'
        })
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'input-field'
        })
    )
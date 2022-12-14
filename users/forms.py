from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.forms import ModelForm
from .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'name', 'nickname',
                'profile_img', 'gender', 'job', 'birth', 'desc']


class FindidForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'birth', 'email']


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','profile_img', 'nickname', 'gender', 'birth', 'job', 'desc', 'email']


class ResetpwForm(PasswordResetForm):
    username = forms.CharField()

    class Meta:
        fields = ['username', 'email']
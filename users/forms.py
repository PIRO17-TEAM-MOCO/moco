from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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
        fields = ['name', 'birth']

class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['profile_img', 'nickname', 'gender', 'birth', 'job', 'desc']
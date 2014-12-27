from django.contrib.auth.models import User
from myreel.models import UserProfile
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()

class AddMovieForm(forms.Form):
    rt_id = forms.CharField(widget=forms.HiddenInput())
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    firstname = forms.CharField(max_length=255, required=False)
    lastname = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username','email', 'firstname', 'lastname', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
        'placeholder':'Username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'placeholder':'Password'
        }
    ))
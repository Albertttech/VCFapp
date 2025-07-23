from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class MemberRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class MemberLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)

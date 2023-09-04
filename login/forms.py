from django import forms
from .models import User

class SignInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'telegram', 'first_name', 'last_name']

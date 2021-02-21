from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())



    class Meta:
        model = Account
        fields = ['username','email','password','confirm_password']


class LoginForm():

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ['email','password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidatinError("invalid credincials")





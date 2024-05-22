from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=500)

    class Meta:
        model = Account
        fields = ("email", "password1", "password2")


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    authenticated_user: Account = None

    class Meta:
        model = Account
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            # cleaned_data = super().clean()
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            self.authenticated_user = authenticate(email=email, password=password)
            if not self.authenticated_user:
                raise forms.ValidationError("Incorrect email or password.")

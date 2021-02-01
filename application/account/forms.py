from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer


class CustomerForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ('name', 'email', 'organization', 'website', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Minimum length of 8 characters."
        self.fields['password2'].label = "Password Confirmation"
        self.fields['password2'].help_text = "Enter the same password for confirmation."


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    # Note: Customer.username == Customer.email
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'ad-launcher-text-field w-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'ad-launcher-text-field w-input'}))

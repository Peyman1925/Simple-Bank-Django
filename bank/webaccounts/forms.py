from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from phonenumber_field.formfields import PhoneNumberField

class SignUpForm(UserCreationForm):
    phone_number = PhoneNumberField(
        region="IR", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+98...'})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    home_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'phone_number', 'email', 'national_id', 'home_address', 'role')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'national_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
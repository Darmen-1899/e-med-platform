from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, FileField

from .models import CustomUser, UserRequest


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control form-floating mb-3', id: "username"}))
    first_name = forms.CharField(label='Your name', widget=forms.TextInput(
        attrs={'class': 'form-control form-floating mb-3 ', id: "name"}))
    last_name = forms.CharField(label='Your last name',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control form-floating mb-3', id: "surname"}))
    after_name = forms.CharField(label='Your patronymic',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control form-floating mb-3', id: "aftername"}))
    iin = forms.CharField(label='IIN', max_length=12,
                          widget=forms.TextInput(attrs={'class': 'form-control form-floating mb-3', id: "aftername"}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control form-floating mb-3', id: "email"}))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control form-floating mb-3', id: "password"}))
    password2 = forms.CharField(label='Password Confirmation',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control form-floating mb-3', id: "repeatpassword"}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'after_name', 'iin', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='User name',
                               widget=forms.TextInput(attrs={'class': 'form-control form-floating mb-3', id: "email"}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control form-floating mb-3', id: "password"}))


class ContactForm(ModelForm):
    class Meta:
        model = UserRequest
        fields = ['name', 'description', 'email']

        widgets = {
            "description": TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': "medicine",
                'placeholder': "Name of the medicine",
            }),
            "email": TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': "medicine",
                'placeholder': "Email",
            }),
            "name": TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': "medicine",
                'placeholder': "Full Name",
            }),
        }


class MedVerify(forms.Form):
    username = forms.CharField(label='The electronic signature that came to your email',
                               widget=forms.TextInput(attrs={'class': 'form-control form-floating mb-3', id: "email"}))

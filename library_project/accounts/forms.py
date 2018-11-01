
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from library_app import models


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')
        model = get_user_model()

    # def __init__(self, *args, **kwargs): #zmiana labela dla username
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].label = 'Display Name'
    #     self.fields['email'].label = 'Email Address'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfileInfo
        fields = ('phone', 'pesel', 'street',
                  'house_number', 'city', 'post_code')
        labels = {
            'phone': 'Telefon',
            'pesel': 'PESEL',
            'street': 'Ulica',
            'house_number': 'Numer domu',
            'city': 'Miasto',
            'post_code': 'Kod pocztowy'
        }

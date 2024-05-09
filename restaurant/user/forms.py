from django import forms

from .models import User

class UserCreationForm(forms.ModelForm):
    email = forms.CharField(max_length=40)
    class Meta:
        model = User
        fields = ['phone_number', 'password', 'username', 'email']
        labels = {'phone_number': 'Введите номер телефона',
                  'password': 'Введите пароль',
                  'username': 'Введите имя пользователя',
                  'email': 'Введите почту'}

class UserLoginForm(forms.Form):

    phone_number = forms.CharField(
        label='Введите номер телефона',
        max_length=15)

    password = forms.CharField(label='Введите пароль')
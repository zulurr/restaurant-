from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


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

    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)

class UserProfileChangeForm(forms.Form):
    phone_number = forms.CharField(
        label='Введите номер телефона',
        max_length=15)
    username = forms.CharField(label='Введите имя пользователя',
                               max_length=50)
    email = forms.EmailField(label='Введите адрес электронной почты',
                             max_length=40)

class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Введите старый пароль',
                                   widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='Введите новый пароль',
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Повторите новый пароль',
                                    widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = self.user
        if not user.check_password(old_password):
            raise ValidationError('Старый пароль записан неверно!')

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        password_validation.validate_password(new_password1)  # Проверка на соответствие правилам создания пароля
        return new_password1

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data['new_password2']
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError("Новые пароли не соответствуют друг другу!")

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
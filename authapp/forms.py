import hashlib
import random
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from django.forms import TextInput
from .models import XabrUser


class XabrUserLoginForm(AuthenticationForm):
    """форма аутентификации пользователя"""

    class Meta:
        model = XabrUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            if field_name == 'password':
                field.widget.attrs['placeholder'] = f'Пароль'
            else:
                field.widget.attrs['placeholder'] = f'Имя пользователя'


class XabrUserRegisterForm(UserCreationForm):
    """форма регистрации пользователя"""

    class Meta:
        model = XabrUser
        fields = ('username', 'first_name', 'email', 'password1', 'password2', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self, commit=True):
        user = super(XabrUserRegisterForm, self).save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class XabrUserEditForm(UserChangeForm):
    """форма редактирования данных пользователя"""

    class Meta:
        model = XabrUser
        fields = ('username', 'first_name', 'email', 'age', 'aboutMe', 'avatar', 'password')
        widgets = {
            'username': TextInput(attrs={'id': 'id_username', 'readonly': 'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

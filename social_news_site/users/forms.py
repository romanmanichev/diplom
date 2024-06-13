from re import match, search
from typing import Any
from django import forms
from django.forms import FileInput
from django.contrib.auth import get_user_model
from django.http import JsonResponse

class LoginForm(forms.ModelForm):
    username = forms.CharField(label='',
        widget=forms.TextInput(attrs={
            'class': 'form__input small',
            'placeholder': 'Логин',
        }))
    
    password = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form__input small',
            'placeholder': 'Пароль',
        }))
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='',
        widget=forms.TextInput(attrs={
            'class': 'form__input username',
            'placeholder': 'Логин',
            'maxlength': '150',
        }))
    password = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form__input password password',
            'placeholder': 'Пароль',
            'maxlength': '128',
        }))
    password2 = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form__input',
            'placeholder': 'Повтор пароля',
            'maxlength': '128',
        }))
    
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'password2']
        
    
    def clean_password(self):
        cd = self.cleaned_data
        if not (search(r'[a-z]', cd['password']) and search(r'[0-9]', cd['password'])):
            self.add_error('password', 'Пароль должен содержать латинские буквы, цифры и не менее 8 символов')
        else:
            return cd['password']
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            self.add_error('password', 'Пароли не совпадают')
        return cd['password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not bool(match(r'[a-zA-Z0-9]{4,}$', username)):
            self.add_error('username', 'Логин должен содержать латинские буквы или цифры и не менее 4 символов')
        elif get_user_model().objects.filter(username=username).exists():
            self.add_error('username', 'Пользователь с таким логином уже существует')
        return username



class ProfileEditForm(forms.ModelForm):
    photo = forms.ImageField(label='', widget=FileInput)
    
    class Meta:
        model = get_user_model()
        fields = ['photo']
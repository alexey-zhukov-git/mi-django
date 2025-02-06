from django import forms
from .models import Order
# from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model
User = get_user_model()

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('title', 'content', 'price')

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control'}
    ))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    captcha = CaptchaField(label='Введите текст с картинки',
        error_messages={'invalid': 'Неправильный текст'})

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

class ChangePasswordForm(forms.Form):
    password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
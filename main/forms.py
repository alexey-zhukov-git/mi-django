from django import forms
from .models import Order
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('title', 'content', 'price')

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    captcha = CaptchaField(label='Введите текст с картинки',
    error_messages={'invalid': 'Неправильный текст'})

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
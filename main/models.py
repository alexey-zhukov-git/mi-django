from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name='Название кейса')
    content = models.TextField(default='', verbose_name='Описание')
    price = models.IntegerField(default=0, verbose_name='Бюджет (руб.)')
    status = models.CharField(verbose_name='status', max_length=50, default='Создано')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    edited_at = models.DateTimeField(auto_now=True)

class UserUniqueToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, unique=True)
    datetime = models.DateTimeField(auto_now_add=True)

class EmailVerificationToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, unique=True)
    datetime = models.DateTimeField(auto_now_add=True)
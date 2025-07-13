from django.urls import path
from .views import index, contacts, profile, privacy

urlpatterns = [
    path('', index),
    #path('contacts/', contacts, name='contacts'),
    path('privacy-policy/', privacy, name='privacy'),
]
from django.urls import path
from .views import index, contacts, profile

urlpatterns = [
    path('', index),
    path('contacts/', contacts),
    #path('profile/', profile)

]
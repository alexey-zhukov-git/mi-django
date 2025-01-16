"""
URL configuration for microint project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main.views import registration, profile, new_order, del_order, view_order
from django.contrib.auth import views as authViews

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('user/registration/', registration, name='registration'),
    path('accounts/logout/', authViews.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/login/', authViews.LoginView.as_view(next_page='/accounts/profile'), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('new/order', new_order, name='new_order'),
    path('delete/<int:pk>', del_order, name='del_order'),
    path('view/<int:pk>', view_order, name='view_order'),
]

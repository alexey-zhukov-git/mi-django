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
from main.views import registration, profile, new_order, view_order, edit_order, undo_order, user_login, change_password, link_to_email, token_auth, blog_index, authorization_via_link, email_verification
from django.contrib.auth import views as authViews
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path('', include('main.urls')),
    path('blog/', blog_index, name='blog_index'),
    path('blog/authorization-via-link', authorization_via_link, name='authorization_via_link'),
    path('admin/', admin.site.urls),
    path('accounts/registration/', registration, name='registration'),
    path('accounts/logout/', authViews.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/login/', user_login, name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/new-order', new_order, name='new_order'),
    path('accounts/view/<int:pk>', view_order, name='view_order'),
    path('accounts/edit/<int:pk>/', edit_order, name='edit_order'),
    path('accounts/undo/<int:pk>/', undo_order, name='undo_order'),
    path('accounts/auth/<str:token>/', token_auth, name='token_auth'),
    path('email-verification/<str:token>/', email_verification, name='email_verification'),
    path('captcha/', include('captcha.urls')),
    path('accounts/change-password/', change_password, name='change_password'),
    path('accounts/link-to-email', link_to_email, name='link_to_email'),
    path('social/', include('social_django.urls', namespace='social')),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
#from django.contrib.auth.forms import UserCreationForm
from .forms import OrderForm, UserRegistrationForm, LoginForm, ChangePasswordForm, TokenToEmailForm
from .models import Order, UserUniqueToken
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
from datetime import timedelta
User = get_user_model()

def index(request):
    total_orders = Order.objects.count()
    cancelled_by_user_orders = Order.objects.filter(status='Отменен заказчиком').count()
    cancelled_by_admin_orders = Order.objects.filter(status='Отменен администратором').count()
    total_cancelled_orders = cancelled_by_user_orders + cancelled_by_admin_orders
    under_consideration_orders = Order.objects.filter(status='На рассмотрении').count()
    in_progress_orders = Order.objects.filter(status='В работе').count()
    done_orders = Order.objects.filter(status='Завершено').count()
    template = loader.get_template('main/home.html')
    context = {
        'total_orders': total_orders,
        'total_cancelled_orders': total_cancelled_orders,
        'under_consideration_orders': under_consideration_orders,
        'in_progress_orders': in_progress_orders,
        'done_orders': done_orders
        }
    return HttpResponse(template.render(context, request))

def contacts(request):
    template = loader.get_template('main/contacts.html')
    context = {}
    return HttpResponse(template.render(context, request))
    
def profile(request):
    id = request.user.id
    orders = Order.objects.filter(user_id=id)
    orders_sum = orders.count()
    template = loader.get_template('main/profile.html')
    context = {'orders': orders, 'orders_sum': orders_sum}
    return HttpResponse(template.render(context, request))

def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            msg = 'Пользователь с email %s зарегистрирован' % new_user.email
            send_mail('Django mail', msg, 'mail@microintervals.ru', ['myshakhovskaya@yandex.ru'], fail_silently=False)
            return render(request, 'main/profile.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'main/registration.html', {'user_form': user_form})
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/accounts/profile/')
            else:
                return render(request, 'registration/login.html', {'error_message': 'Your account has been disabled'}, {'login_form': LoginForm()})
        else:
            return render(request, 'registration/login.html', {'error_message': 'Неверное имя пользователя или пароль', 'login_form': LoginForm()})
    login_form = LoginForm()
    return render(request, 'registration/login.html', {'login_form': login_form})

def new_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user.id
            post.save()
            msg = 'На сайте создан новый кейс. Создал пользователь %s. Название кейса: %s' % request.user.email % request.user.email
            send_mail('Django mail', msg, 'mail@microintervals.ru', ['myshakhovskaya@yandex.ru'], fail_silently=False)
            return redirect('/accounts/profile/', pk=post.pk)
    else:
        form = OrderForm()
        return render(request, 'main/new_order.html', {'form': form})

def view_order(request, pk):
    if request.user.is_authenticated and request.user.id == Order.objects.get(pk=pk).user_id:
        order = Order.objects.get(pk=pk)
        return render(request, 'main/view_order.html', {'order': order})
    else:
        return redirect('/')

def edit_order(request, pk):
    if request.user.is_authenticated and request.user.id == Order.objects.get(pk=pk).user_id:
        order = Order.objects.get(pk=pk)
        if request.method == 'POST':
            form = OrderForm(request.POST, request.FILES, instance=order)
            if form.is_valid():
                order = form.save()
                return redirect('/accounts/profile/')
        else:
            form = OrderForm(instance=order)
            context = {'form': form,}
            return render(request, 'main/edit_order.html', context)
    else:
        return redirect('/')

def undo_order(request, pk):
    if request.user.is_authenticated and request.user.id == Order.objects.get(pk=pk).user_id:
        order = Order.objects.get(pk=pk)
        order.status = 'Отменен заказчиком'
        order.save()
        return redirect('/accounts/profile/')
    else:
        return redirect('/')

def privacy(request):
    template = loader.get_template('main/privacy-policy.html')
    context = {}
    return HttpResponse(template.render(context, request))

def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                user = request.user
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('/accounts/profile/')
        else:
            form = ChangePasswordForm()
            user = request.user
            return render(request, 'main/change_password.html', {'form': form, 'user': user})
    else:
        return redirect('/')

def link_to_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user_email = user.email
            user_id = user.id
            token = uuid.uuid4().hex
            UserUniqueToken.objects.create(user_id=user_id, token=token)
            msg = 'Ваша ссылка для авторизации: https://microintervals.ru/accounts/auth/%s Ссылка действительна 2 часа.' % token
            send_mail('Django mail', msg, 'mail@microintervals.ru', ['%s' % user_email], fail_silently=False)
            return render(request, 'main/link_to_email_success.html', {'user_email': user_email})
        else:
            return render(request, 'main/link_to_email_error.html')
    else:
        form = TokenToEmailForm()
        return render(request, 'main/link_to_email.html', {'form': form})

def token_auth(request, token):
    if UserUniqueToken.objects.filter(token=token).exists():
        time_now = timezone.now()
        token_time = UserUniqueToken.objects.get(token=token).datetime
        if token_time < (time_now - timedelta(hours=2)):
            return render(request, 'main/token_auth_error.html')
        else:
            user_id = UserUniqueToken.objects.get(token=token).user_id
            user = User.objects.get(id=user_id)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/accounts/profile/')
    else:
        return render(request, 'main/404.html')
    
def blog_index(request):
    return render(request, 'blog/index.html')

def authorization_via_link(request):
    return render(request, 'blog/authorization_via_link.html')
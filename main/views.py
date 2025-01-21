from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import OrderForm, UserRegistrationForm
from .models import Order
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def index(request):
    template = loader.get_template('main/home.html')
    context = {}
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
    title = 'Главная страница'
    context = {'orders': orders, 'title': title, 'orders_sum': orders_sum}
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
            send_mail('Django mail', msg, 'mail@microintervals.ru', ['a@core-i5.ru'], fail_silently=False)
            return render(request, 'main/profile.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'main/registration.html', {'user_form': user_form})
    
def new_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user.id
            post.save()
            msg = 'На сайте создан новый кейс. Создал пользователь %s' % request.user.email
            send_mail('Django mail', msg, 'mail@microintervals.ru', ['a@core-i5.ru'], fail_silently=False)
            return redirect('/accounts/profile/', pk=post.pk)
    else:
        form = OrderForm()
        return render(request, 'main/new_order.html', {'form': form})

def del_order(request, pk):
    if request.user.is_authenticated and request.user.id == Order.objects.get(pk=pk).user_id:
        order = Order.objects.get(pk=pk)
        order.delete()
        return redirect('/accounts/profile/')
    else:
        return redirect('/')

def view_order(request, pk):
    if request.user.is_authenticated and request.user.id == Order.objects.get(pk=pk).user_id:
        order = Order.objects.get(pk=pk)
        return render(request, 'main/view_order.html', {'order': order})
    else:
        return redirect('/')
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import OrderForm, SignUpForm
from .models import Order

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # получаем имя пользователя и пароль из формы
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # выполняем аутентификацию
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'main/registration.html', {'form': form})

def new_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user.id
            post.save()
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
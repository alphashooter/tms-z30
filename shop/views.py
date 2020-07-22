from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View
from shop.models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.shortcuts import resolve_url

# Create your views here.


class Index(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        items = Item.objects.all()
        return render(request, 'index.html', {'items': items})


class Product(View):
    def get(self, request: HttpRequest, product_id: int) -> HttpResponse:
        item = Item.objects.get(pk=product_id)
        amount = 0
        user = request.user
        if user.is_authenticated:
            order = Order.objects.filter(user=user).first()
            if order:
                order_item = OrderItem.objects.filter(order=order, item_id=product_id).first()
                if order_item:
                    amount = order_item.amount
        return render(request, 'product.html', {'product': item, 'amount': amount})


class Login(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': True})


class Logout(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect('/')


class Register(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'register.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Пароли не совпадают'})
        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            return render(request, 'register.html', {'error': 'Такое имя уже существует'})
        login(request, user)
        return redirect('/')


class Cart(View):
    def post(self, request: HttpRequest, product_id: int) -> HttpResponse:
        amount = int(request.POST['amount'])
        user: User = request.user
        if user.is_authenticated:
            if amount == 0:
                order = user.order
                if order:
                    OrderItem.objects.filter(order=order, item_id=product_id).delete()
            elif amount > 0:
                order = Order.objects.get_or_create(user=user, name='x', tel='x', address='x')[0]
                item = OrderItem.objects.filter(order=order, item_id=product_id).first()
                if item:
                    item.amount = amount
                    item.save()
                else:
                    OrderItem.objects.create(order=order, item_id=product_id, amount=amount)
        return redirect(resolve_url('product', product_id=product_id))

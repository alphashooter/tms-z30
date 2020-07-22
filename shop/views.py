from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View
from shop.models import *
from django.contrib.auth import login, logout, authenticate

# Create your views here.


class Index(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        items = Item.objects.all()
        return render(request, 'index.html', {'items': items})


class Product(View):
    def get(self, request: HttpRequest, product_id: int) -> HttpResponse:
        item = Item.objects.get(pk=product_id)
        return render(request, 'product.html', {'product': item})


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

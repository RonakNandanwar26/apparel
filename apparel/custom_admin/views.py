from django.shortcuts import render,redirect
from django.conf import settings
import sqlite3
import os
from django.contrib.auth.models import User
from Home.models import Profile
from django.http import HttpResponse
from products.models import Product

# Create your views here.
def home(request):
    if request.session.get('admin'):
        template = 'custom_admin/index.html'
        return render(request,template)
    else:
        return redirect('Admin:login')


def users(request):
    template = 'custom_admin/users.html'
    if request.session.get('admin'):
        users = User.objects.all()
        return render(request,template,{'users':users})
    else:
        return redirect('Admin:login')


def login(request):
    template = 'custom_admin/login.html'
    if request.method == 'POST':
        user = request.POST['username']
        pwd = request.POST['password']
        if user=='admin' and pwd=='admin':
            request.session['admin'] = user
            return redirect('Admin:home')

    return render(request,template)


def logout(request):
    template = 'custom_admin/logout.html'
    if request.session.get('admin') != None:
        request.session.delete()
    else:
        return redirect('Admin:login')

    return render(request,template)


def profile(request,pk):
    template = 'custom_admin/user_profile.html'
    if request.session.get('admin'):
        user = User.objects.get(pk=pk)
        return render(request,template,{'user':user})
    else:
        return redirect('Admin:login')


def user_products(request,pk):
    template = 'custom_admin/user_products.html'
    if request.method == 'POST':
        if request.session.get('admin'):

            print('I am admin')
            usr = User.objects.get(pk=pk)
            print(usr)
            products = Product.objects.filter(user__username=usr.username)
            print(list(products))
            return render(request,template,{'products':products})

    return HttpResponse(1)


from django.shortcuts import render,redirect
from django.conf import settings
import sqlite3
import os
from django.contrib.auth.models import User
from Home.models import Profile
from django.http import HttpResponse,HttpResponseRedirect
from products.models import Product
from .forms import CatForm
from products.models import Category
from django.contrib import messages
import csv
import datetime

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum

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



def add_cat(request):
    if request.session.get('admin'):
        if request.method == "POST":
            form = CatForm(request.POST or None)
            print('before valid')
            if form.is_valid():
                print('form valid')
                form.save()
                messages.success(request, "Category is added Successfully..")
                return redirect('Admin:home')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = CatForm()
        template = 'custom_admin/add_cat.html'
        return render(request, template, {'form': form})
    else:
        return redirect('Admin:login')
#
# def ratings(request,pk):
#     url = request.META.get('HTTP_REFERER')
#     if request.method == "POST":
#         form = Rating_Form(request.POST)
#         if form.is_valid():
#             data = Ratings()
#             data.subject = request.POST['subject']
#             data.comment = request.POST['comment']
#             data.rate = request.POST['rate']
#             data.product_id = pk
#             usr = request.user
#             data.user_id = usr.id
#             data.save()
#             messages.success(request,'Your Review submitted successfully')
#             return HttpResponseRedirect(url)
#     else:
#         return redirect('account_login')


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=users' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    users = User.objects.all()
    writer.writerow(['Username','Email'])
    for user in users:
        writer.writerow([user.username,user.email])

    return response


# export pdf
# pip install WeasyPrint


def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=users' + str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    users = User.objects.all()

    html_string = render_to_string('custom_admin/user_pdf.html',{'users':users})
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name,'rb')
        response.write(output.read())

    return response


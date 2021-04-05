from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Vendor_register
from django.conf import settings
from django.core.mail import send_mail
from .forms import forgot_password_form,otp_match_form
from django.contrib.auth import authenticate
from django.http import HttpResponse
import random
from django.contrib.auth.hashers import check_password

# Create your views here.
def register(request):
    print('before post')
    if request.method == 'POST':
        print('Entered in post')
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        print('before if')
        if (password == confirm_password):
            print('entered')
            usr = User.objects.create_user(name,email,password)
            usr.is_active = False
            usr.save()
            request.session['vendor_email'] = email
            request.session['vendor_name'] = name
            reg = Vendor_register(user=usr)
            reg.save()
            subject = 'Hello ' + name + ' from apparel_vendor!'
            message = "Hello, " + name + ". Welcome To apparel. Please Verify Your Email ID ::--> " "http://127.0.0.1:8000/vendor/confirm_email"
            email_from = settings.EMAIL_HOST_USER
            email_to = [email, ]
            send_mail(subject, message, email_from, email_to)
            return redirect('Vendor:please_verify')
        else:
            messages.error(request,'{}, Please correct the error below...'.format(name))
    template = 'vendor/account/register.html'
    return render(request,template)



def please_verify(request):
    template = 'vendor/account/verification_sent.html'
    return render(request,template)


def confirm_email(request):
    template = 'vendor/account/confirm_email.html'
    email = request.session.get("vendor_email")
    usr = User.objects.get(email=email)
    usr.is_active = True
    usr.is_staff = True
    usr.save()

    vendor = {'name':usr.username, 'email': usr.email}
    request.session['vendor'] = vendor
    if (usr.is_staff == True):
        request.session.get('vendor')
        return redirect('Vendor:home')

    return render(request,template)

def home(request):
    template = 'vendor/index.html'
    if request.session.get('vendor') == None:
        return redirect('Vendor:login')

    return render(request, template)



def login(request):
    print('before post')
    if request.method == 'POST':
        print('after post')
        user = request.POST['username']
        pwd = request.POST['password']

        usr = authenticate(username=user,password=pwd)
        print(usr)
        if usr:
            usr = User.objects.get(username=user)
            print('checking staff status')
            if (usr.is_staff == True):
                print('staff status true')
                print(usr)
                vendor = {'vendor_name':usr.username,'vendor_email':usr.email}
                request.session['vendor'] = vendor
                request.session['vendor_email'] = usr.email
                return redirect('Vendor:home')
            else:
                print('staff status false')
                messages.error(request,'You have no vendor account...')
                return render(request,'account/login.html')

    return render(request,'vendor/account/login.html')



def logout(request):
    template = 'vendor/account/logout.html'
    if (request.session.get('vendor') != None):
        request.session.delete()
    else:
        return redirect('Vendor:login')

    return render(request,template)



def forgot_password(request):
    template = 'vendor/account/forgot_password.html'
    if request.method == 'POST':
        f_p_form = forgot_password_form(request.POST)
        if f_p_form.is_valid():
            email = request.POST.get('email')
            is_email = User.objects.filter(email__iexact=email).exists()
            if is_email:
                OTP = random.randint(111111,999999)
                subject = "Password Reset OTP @apparel_vendor"
                message = "Your OTP is, " + str(OTP) + " .Please Follow This Link, --> http://127.0.0.1:8000/vendor/otp_verify"
                email_from = settings.EMAIL_HOST_USER
                email_to = [email, ]
                send_mail(subject, message, email_from, email_to)

                # OTP and email set In Session
                request.session["reset_password_OTP"] = OTP
                request.session["reset_password_EMAIL"] = email
                return redirect('Vendor:otp_sent')
    else:
        f_p_form = forgot_password_form()

    return render(request,template,{'form':f_p_form})


def otp_sent(request):
    template = 'vendor/account/otp_sent.html'
    return render(request,template)


def otp_verify(request):
    template = 'vendor/account/otp_verification.html'
    if request.method == 'POST':
        otp = request.POST['otp']
        session_otp = request.session.get('reset_password_OTP')
        if str(otp) == str(session_otp):
            return redirect('Vendor:reset_password')
    else:
        messages.error(request,'Please correct the error below...')

    return render(request,template)


def reset_password(request):
    template = 'vendor/account/reset_password.html'
    if request.method == 'POST':
        password = request.POST['password1']
        c_password = request.POST['password2']

        if password == c_password:
            email = request.session.get('reset_password_EMAIL')
            usr = User.objects.get(email=email)
            usr.set_password(password)
            usr.save()
            request.session.delete()
            return redirect('Vendor:login')

    return render(request,template)

def change_password(request):
    template = 'vendor/account/change_password.html'
    if request.session.get('vendor') == None:
        return redirect('Vendor:login')

    elif request.method == 'POST':
        print('in post')
        old = request.POST['password']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        if pass1 == pass2:
            if 'vendor' in request.session:
                print('got session')
                email = request.session.get('vendor_email')
                print(email)

                usr = User.objects.get(email__iexact=email)
                if check_password(old,usr.password):
                    print('old and new same')
                    usr.set_password(pass1)
                    usr.save()
                    request.session.delete()
                    return redirect('Vendor:login')
    return render(request,template)
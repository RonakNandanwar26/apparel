from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
# Create your views here.

def validate_username_signup(request):
    user = request.POST.get('username', '')
    email = request.POST.get('email', '')
    password1 = request.POST.get('password1', '')
    password2 = request.POST.get('password2', '')
    is_taken1 = User.objects.filter(username__iexact=user).exists()
    is_taken2 = User.objects.filter(email__iexact=email).exists()
    if user != '' and email != '' and password1 != '' and password2 != '':
        if not is_taken1 and not is_taken2 and (password1 == password2):
             data = {
                        'is_taken': False,
                        'content': True,
                    }
        else:
            if is_taken1 and is_taken2:
                data = {
                        'is_taken': True,
                        'content': True,
                }
                data['error_message'] = 'username and email already exist'
            elif is_taken1:
                data = {
                    'is_taken': True,
                    'content': True,
                }
                data['error_message'] = 'username already exist'
            else:
                data = {
                    'is_taken': True,
                    'content': True,
                }
                data['error_message'] = 'email already exist'
        return JsonResponse(data)


def validate_username_login(request):
    user = request.POST.get('login', '')
    password = request.POST.get('password', '')
    is_taken = User.objects.filter(username__iexact=user).exists()
    if user != '' and password != '':
        if is_taken:
            user = authenticate(username=user, password=password)
            if user:
                data = {
                    'is_taken': True,
                    'user': True,
                    'content': True,
                }
            else:
                data = {
                    'is_taken': True,
                    'user': False,
                    'content': True,
                }
                data['error_message'] = 'Please enter valid password'
            return JsonResponse(data)
        else:
            data = {'is_taken': False, 'user': False, 'content': True}
            data['error_message'] = 'Please enter valid Username!'
            return JsonResponse(data)
    else:
        data = {
            'content': False
        }
        return JsonResponse(data)



def validate_user_password_reset(request):
    email = request.POST.get('email', '')
    is_taken = User.objects.filter(email__iexact=email).exists()
    if not is_taken:
        data = {
            'is_taken': False,
            'content': True,
        }
        data['error_message'] = 'Please enter existant email address'
    return JsonResponse(data)


def validate_user_password_change(request):
    old = request.POST.get('oldpassword', '')
    new = request.POST.get('password1', '')
    New = request.POST.get('password2', '')
    if old != '' and new != '' and New != '':
        if check_password(old, request.user.password):
            data = {
                'content': True,
                'success': True
            }
            return JsonResponse(data)
        else:
            data = {
                'content': True,
                'success': False
            }
            data['error_message'] = 'Please enter correct current password'
            return JsonResponse(data)
    else:
        data = {
            'content': False
        }
        return JsonResponse(data)


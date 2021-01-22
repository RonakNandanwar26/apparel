from django.urls import path
from .views import register,login,please_verify,confirm_email,home,logout,forgot_password,reset_password,otp_verify,otp_sent,change_password

app_name = 'Vendor'

urlpatterns = [
    path('',register,name='register'),
    path('login/',login,name='login'),
    path('verify/',please_verify,name='please_verify'),
    path('confirm_email/',confirm_email,name='confirm_email'),
    path('home/',home,name='home'),
    path('logout/',logout,name='logout'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('otp_sent',otp_sent,name='otp_sent'),
    path('otp_verify',otp_verify,name='otp_verify'),
    path('reset_password/',reset_password,name='reset_password'),
    path('change_password/',change_password,name='change_password'),
]
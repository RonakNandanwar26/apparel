from django.urls import path
from .views import home,users,login,logout,profile,user_products,add_cat

app_name = 'Admin'

urlpatterns = [
    path('',home,name='home'),
    path('users/',users,name='users'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('user_profile/<int:pk>',profile,name='profile'),
    path('user_products/<int:pk>',user_products,name='user_products'),
    path('add_cat/',add_cat,name='add_cat'),
]
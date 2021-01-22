from django.urls import path
from .views import *

app_name = 'Authentication'

urlpatterns = [
    path('ajax/validate_username/signup', validate_username_signup, name='validate_username_signup'),
    path('ajax/validate_username/login/', validate_username_login, name='validate_username_login'),
    path('ajax/validate_user/password_reset', validate_user_password_reset, name='validate_user_password_reset'),
    path('ajax/validate_user/password_change/', validate_user_password_change, name='validate_user_password_change'),
]
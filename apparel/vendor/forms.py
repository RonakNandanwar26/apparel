from django import forms
from .models import Vendor_register
from django.contrib.auth.models import User


class forgot_password_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']



class otp_match_form(forms.ModelForm):
    otp = forms.CharField(max_length = 6, widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your OTP'}))

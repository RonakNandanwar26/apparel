from .models import *
from django import forms

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"



class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=20, disabled=True, widget=forms.TextInput(
        attrs={
            'class' : 'form-control'
        }
    ))

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class' : 'form-control'
    }))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={
            'class' : 'form-control'
        }
    ))
    email = forms.EmailField(max_length=50, disabled=True, widget=forms.EmailInput(
        attrs={
            'class' : 'form-control'
        }
    ))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'address', 'tel', 'gender', 'age', 'file')
        widgets={
            'bio' : forms.Textarea(attrs={'class':'form-control'}),
            'tel' : forms.NumberInput(attrs={'class':'form-control'}),
            'age' : forms.NumberInput(attrs={'class':'form-control'}),
            'address' : forms.Textarea(attrs={'class':'form-control'}),
            'gender' : forms.Select(attrs={'class':'form-control'})
        }


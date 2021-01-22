from .models import Product
from django import forms

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ('name', 'description', 'category', 'gender', 'price', 'quantity', 'features', 'image1', 'image2', 'image3','image4')
		widgets = {
			'name':forms.TextInput(attrs={'class':'form-control'}),
			'description':forms.Textarea(attrs={'class':'form-control'}),
			'category':forms.Select(attrs={'class':'form-control'}),
			'gender':forms.Select(attrs={'class':'form-control'}),
			'price':forms.TextInput(attrs={'class':'form-control'}),
			'quantity':forms.TextInput(attrs={'class':'form-control'}),
			'features':forms.Textarea(attrs={'class':'form-control'})
		}
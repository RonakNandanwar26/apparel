from django import forms
from products.models import Category


class CatForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

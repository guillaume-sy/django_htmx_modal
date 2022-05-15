from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['product_reg_date', 'product_creating_user', 'product_factory_name']

# forms.py

from django import forms
from .models import AgriculturalProduct

class AgriculturalProductForm(forms.ModelForm):
    class Meta:
        model = AgriculturalProduct
        fields = ['name', 'description', 'image', 'price', 'category']
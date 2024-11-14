# myapp/admin.py
from django.contrib import admin
from .models import AgriculturalProduct
from .models import Category

admin.site.register(AgriculturalProduct)
admin.site.register(Category)
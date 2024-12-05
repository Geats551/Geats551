# myapp/admin.py
from django.contrib import admin
from .models import AgriculturalProduct
from .models import Category
from .models import Comment
from .models import Purchase

admin.site.register(Comment)
admin.site.register(AgriculturalProduct)
admin.site.register(Category)
admin.site.register(Purchase)
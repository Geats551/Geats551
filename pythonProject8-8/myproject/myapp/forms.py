# forms.py

from django import forms
from .models import AgriculturalProduct
from .models import Comment

class AgriculturalProductForm(forms.ModelForm):
    class Meta:
        model = AgriculturalProduct
        fields = ['name', 'description', 'image', 'price', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # 我们只允许用户填写评论内容
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 50, 'placeholder': '请输入你想评论的内容'}),
        }

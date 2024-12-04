
from django.db import models
from django.contrib.auth import get_user_model

class Category(models.Model):  
    name = models.CharField(max_length=100, unique=True)  
    description = models.TextField(blank=True)  

    class Meta:  
        verbose_name_plural = 'Categories'  

    def __str__(self):  
        return self.name  

class AgriculturalProduct(models.Model):


    name = models.CharField(max_length=200)  
    description = models.TextField()  
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # 使用 ImageField  
    price = models.DecimalField(max_digits=5, decimal_places=2)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    click_count = models.IntegerField(default=0)

    def __str__(self):  
        return self.name



User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agricultural_product = models.ForeignKey(AgriculturalProduct, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}\'s comment on {self.agricultural_product.name}'

User = get_user_model()

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agricultural_product = models.ForeignKey(AgriculturalProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # 购买数量
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)  # 新增字段，标记是否取消

    def __str__(self):
        return f'{self.user.username} 购买了 {self.quantity} 个 {self.agricultural_product.name} 于 {self.purchase_date}'
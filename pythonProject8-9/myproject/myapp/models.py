from django.db import models  

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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)  

    def __str__(self):  
        return self.name
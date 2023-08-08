from django.db import models


class AdmCategories(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ProductColor(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class ProductSize(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class AdmProducts(models.Model):
    name = models.CharField(max_length=50, unique=True)
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    brand = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(AdmCategories, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return self.name    

class ProductVariant(models.Model):
    product = models.ForeignKey(AdmProducts, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='variant_images/', blank=True, null=True)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size.name}"




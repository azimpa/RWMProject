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
    brand = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(AdmCategories, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    colors = models.ManyToManyField(ProductColor)
    sizes = models.ManyToManyField(ProductSize)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return self.name    

class ProductVariant(models.Model):
    product = models.ForeignKey(AdmProducts, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active'
    )

    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size.name}"




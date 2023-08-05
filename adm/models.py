from django.db import models

class AdmCategories(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class AdmProducts(models.Model):
    name = models.CharField(max_length=50, unique=True)
    brand = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(AdmCategories, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return self.name
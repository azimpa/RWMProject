from django.db import models
from accounts.models import CustomUser

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="House or Company Name")
    postoffice = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)

    def __str__(self):
        return self.user
from django.shortcuts import render, redirect
from adm.models import AdmProducts
from django.views.decorators.cache import never_cache

# Create your views here.


@never_cache
def home(request):
    products = AdmProducts.objects.all()
    return render(request, "user/home.html", {"prod": products})

def product(request):
    return render(request, "user/product.html")


def base_user(request):
    return render(request, "user/base_user.html")

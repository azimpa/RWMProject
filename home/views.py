from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from adm.models import AdmProducts

# Create your views here.

def home(request):
    products = AdmProducts.objects.all()
    return render(request, "user/home.html", {'prod' : products})

def categories(request):
    return render(request, "user/categories.html")

def contact(request):
    return render(request, "user/contact.html")

def product(request):
    return render(request, "user/product.html")



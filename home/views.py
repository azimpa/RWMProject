from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, "user/home.html")

@login_required
def categories(request):
    return render(request, "user/categories.html")

def contact(request):
    return render(request, "user/contact.html")



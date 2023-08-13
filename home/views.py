from django.shortcuts import render, redirect, get_object_or_404
from home.models import Address
from django.contrib.auth import logout
from adm.models import AdmProducts,AdmCategories

# Create your views here.

def home(request):
    products = AdmProducts.objects.all()
    if request.user.is_anonymous:
        return render(request, "user/home.html", {'products': products})
    elif request.user.is_superuser:
        logout(request)
        return render(request, "user/home.html", {'products': products})
    else:
        products = AdmProducts.objects.all()
        print(products)
        return render(request, "user/home.html", {'products': products})

def total_products(request):
    product = AdmProducts.objects.all()
    print(product)
    return render(request, "user/total_products.html",{'products': product})    


def roadbikes(request):
    category = AdmCategories.objects.get(name='road_bikes')
    products = AdmProducts.objects.filter(category=category)
    print(products)
    return render(request, "user/roadbikes.html", {'products': products})

def gravelbikes(request):
    category = AdmCategories.objects.get(name='gravel_bikes')
    products = AdmProducts.objects.filter(category=category)
    print(products)
    return render(request, "user/gravelbikes.html", {'products': products})

def hybridbikes(request):
    category = AdmCategories.objects.get(name='hybrid_bikes')
    products = AdmProducts.objects.filter(category=category)
    print(products)
    return render(request, "user/hybridbikes.html", {'products': products})

def mountainbikes(request):
    category = AdmCategories.objects.get(name='mountain_bikes')
    products = AdmProducts.objects.filter(category=category)
    print(products)
    return render(request, "user/mountainbikes.html", {'products': products})

def product_description(request,id):
    product = AdmProducts.objects.get(id=id)
    print(product)
    return render(request, "user/product_description.html",{'products': product})

def useraddress(request):
    user = request.user
    address = Address.objects.filter(user=user)
    return render(request, "user/useraddress.html", {"addresses": address})

def add_address(request):
    if request.method == "POST":
        housename_companyname = request.POST.get("Housename_companyname")
        post_office = request.POST.get("Post_office")
        street = request.POST.get("Street")
        city = request.POST.get("City")
        state = request.POST.get("State")
        country = request.POST.get("Country")
        pin_code = request.POST.get("Pin_code")

        address = Address(
            user=request.user,
            name=housename_companyname,
            postoffice=post_office,
            street=street,
            city=city,
            state=state,
            country=country,
            pin_code=pin_code,
        )
        address.save()

        return redirect("useraddress")

    return render(request, "user/add_address.html")

def edit_address(request, id):
    address = get_object_or_404(Address, id = id, user = request.user)

    if request.method == "POST":
        housename_companyname = request.POST.get("Edited_Housename_companyname")
        post_office = request.POST.get("Edited_Post_office")
        street = request.POST.get("Edited_Street")
        city = request.POST.get("Edited_City")
        state = request.POST.get("Edited_State")
        country = request.POST.get("Edited_Country")
        pin_code = request.POST.get("Edited_Pin_code")

        address.name = housename_companyname
        address.postoffice = post_office
        address.street = street
        address.city = city
        address.state = state
        address.country = country
        address.pin_code = pin_code
        address.save()

        return redirect('useraddress')

    return render(request, "user/edit_address.html", {'address': address})

def delete_address(request, id):
    address = get_object_or_404(Address, id=id)
    address.delete()
    return redirect("useraddress")

def cart(request):
    return render(request, "user/cart.html")

def checkout(request):
    return render(request, "user/checkout.html")
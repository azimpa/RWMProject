from django.shortcuts import render, redirect, get_object_or_404
from adm.models import AdmProducts
from home.models import Address
from accounts.models import CustomUser
from django.views.decorators.cache import never_cache
from django.http import HttpResponseBadRequest

# Create your views here.


@never_cache
def home(request):
    products = AdmProducts.objects.all()
    return render(request, "user/home.html", {"prod": products})


def product(request):
    return render(request, "user/product.html")


def useraddress(request):
    user = request.user
    address = Address.objects.filter(user=user)
    return render(request, "user/useraddress.html", {"addresses": address})


def add_address(request):
    if request.method == "POST":
        house_name = request.POST.get("House_name")
        post_office = request.POST.get("Post_office")
        street = request.POST.get("Street")
        city = request.POST.get("City")
        state = request.POST.get("State")
        country = request.POST.get("Country")
        pin_code = request.POST.get("Pin_code")

        address = Address(
            user=request.user,
            house_name=house_name,
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


def delete_address(request, id):
    address = get_object_or_404(Address, id=id)
    address.delete()
    return redirect("useraddress")

def edit_address(request, id):
    address = get_object_or_404(Address, id = id, user = request.user)

    if request.method == "POST":
        house_name = request.POST.get("Edited_House_name")
        post_office = request.POST.get("Edited_Post_office")
        street = request.POST.get("Edited_Street")
        city = request.POST.get("Edited_City")
        state = request.POST.get("Edited_State")
        country = request.POST.get("Edited_Country")
        pin_code = request.POST.get("Edited_Pin_code")

        address.house_name = house_name
        address.postoffice = post_office
        address.street = street
        address.city = city
        address.state = state
        address.country = country
        address.pin_code = pin_code
        address.save()

        return redirect('useraddress')

    return render(request, "user/edit_address.html", {'address': address})

from django.shortcuts import render, redirect, get_object_or_404
from home.models import Address
from django.contrib.auth import logout
from django.contrib import messages
from urllib.parse import unquote
from adm.models import AdmProducts, AdmCategories
from home.models import Cartitem, Cart

# Create your views here.


def home(request):
    products = AdmProducts.objects.all()
    if request.user.is_anonymous:
        return render(request, "user/home.html", {"products": products})
    elif request.user.is_superuser:
        logout(request)
        return render(request, "user/home.html", {"products": products})
    else:
        products = AdmProducts.objects.all()
        return render(request, "user/home.html", {"products": products})


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
    address = get_object_or_404(Address, id=id, user=request.user)

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

        return redirect("useraddress")

    return render(request, "user/edit_address.html", {"address": address})


def delete_address(request, id):
    address = get_object_or_404(Address, id=id)
    address.delete()
    return redirect("useraddress")


def total_products(request):
    product = AdmProducts.objects.all()
    return render(request, "user/total_products.html", {"products": product})


def roadbikes(request):
    category = AdmCategories.objects.get(name="road_bikes")
    products = AdmProducts.objects.filter(category=category)
    return render(request, "user/roadbikes.html", {"products": products})


def gravelbikes(request):
    category = AdmCategories.objects.get(name="gravel_bikes")
    products = AdmProducts.objects.filter(category=category)
    print(products)
    return render(request, "user/gravelbikes.html", {"products": products})


def hybridbikes(request):
    category = AdmCategories.objects.get(name="hybrid_bikes")
    products = AdmProducts.objects.filter(category=category)
    print(products)
    return render(request, "user/hybridbikes.html", {"products": products})


def mountainbikes(request):
    category = AdmCategories.objects.get(name="mountain_bikes")
    products = AdmProducts.objects.filter(category=category)
    return render(request, "user/mountainbikes.html", {"products": products})


def product_description(request, id):
    product = AdmProducts.objects.get(id=id)
    return render(request, "user/product_description.html", {"products": product})


def add_to_cart(request, id):
    user = request.user
    product = AdmProducts.objects.get(id=id)

    # Check if the user already has a cart, if not create one
    cart, created = Cart.objects.get_or_create(user=user)

    # Check if the product is already in the cart
    try:
        cart_item = Cartitem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1  # Increment the quantity if already in the cart
        cart_item.save()
        messages.success(request, f"{product.name} quantity updated in your cart.")
    except Cartitem.DoesNotExist:
        cart_item = Cartitem(cart=cart, product=product)
        cart_item.save()
        messages.success(request, f"{product.name} added to your cart.")

    return redirect("cart")


def cart(request):
    user = request.user
    cart_items = Cartitem.objects.filter(cart__user=user)

    total_price = 0
    final_total = 0  # Initialize final_total with a default value

    for item in cart_items:
        # Calculate offer price for the product
        item.offer_price = item.product.productvariant_set.first().offer_price

        # Calculate total price for the item (product * quantity)
        item.total_price_each = item.offer_price * item.quantity

        # Add the item's total price to the overall total price
        total_price += item.total_price_each

    # Calculate the final total after the loop
    final_total = total_price + 1000

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "final_total": final_total,
    }

    return render(request, "user/cart.html", context)


def update_cart_item(request, id):
    cart_item = get_object_or_404(Cartitem, pk=id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "increase":
            if cart_item.quantity < cart_item.product.productvariant_set.first().stock:
                cart_item.quantity += 1
            else:
                messages.warning(request, "Out of stock")
        elif action == "decrease":
            cart_item.quantity = max(cart_item.quantity - 1, 1)

        cart_item.save()

    return redirect("cart")


def clear_cart_item(request):
    user = request.user
    cart = Cart.objects.get(user=user)

    # Delete all cart items associated with the user's cart
    Cartitem.objects.filter(cart=cart).delete()

    messages.success(request, "Your cart has been cleared.")
    return redirect("cart")


def delete_cart_item(request, id):
    user = request.user
    cart = Cart.objects.get(user=user)

    try:
        cart_item = Cartitem.objects.get(cart=cart, id=id)
        cart_item.delete()
        messages.success(
            request, f"{cart_item.product.name} has been removed from your cart."
        )
    except Cartitem.DoesNotExist:
        messages.error(request, "Cart item not found.")

    return redirect("cart")


def checkout(request):
    user = request.user
    address = Address.objects.filter(user=user)
    cart_items_param = request.GET.get("cart_items")

    if cart_items_param == "true":
        cart = Cart.objects.get(user=user)  # Query the cart for the current user
        cart_items = Cartitem.objects.filter(cart=cart)

        total_price = 0
        final_total = 0  # Initialize final_total with a default value

        for item in cart_items:
            # Calculate offer price for the product
            item.offer_price = item.product.productvariant_set.first().offer_price

            # Calculate total price for the item (product * quantity)
            item.total_price_each = item.offer_price * item.quantity

            # Add the item's total price to the overall total price
            total_price += item.total_price_each

        # Calculate the final total after the loop
        final_total = total_price + 1000

        return render(
            request,
            "user/checkout.html",
            {
                "addresses": address,
                "cart_items": cart_items,
                "total_price": total_price,
                "final_total": final_total,
            },
        )

    return render(request, "user/checkout.html", {"addresses": address})


def add_checkout_address(request):
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

        return redirect("checkout")

    return render(request, "user/add_checkout_address.html")


def edit_checkout_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)

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

        return redirect("checkout")

    return render(request, "user/edit_checkout_address.html", {"address": address})


def delete_checkout_address(request, id):
    address = get_object_or_404(Address, id=id)
    address.delete()
    return redirect("checkout")


def order_summary(request):
    return render(request, "user/order_summary.html")

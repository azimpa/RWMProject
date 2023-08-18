from django.shortcuts import render, redirect, get_object_or_404
from home.models import Address
from django.contrib.auth import logout
from django.contrib import messages
from urllib.parse import unquote
from adm.models import AdmProducts, AdmCategories
from home.models import Cartitem, Cart, Order, OrderItem

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
    return render(request, "user/gravelbikes.html", {"products": products})


def hybridbikes(request):
    category = AdmCategories.objects.get(name="hybrid_bikes")
    products = AdmProducts.objects.filter(category=category)
    return render(request, "user/hybridbikes.html", {"products": products})


def mountainbikes(request):
    category = AdmCategories.objects.get(name="mountain_bikes")
    products = AdmProducts.objects.filter(category=category)
    return render(request, "user/mountainbikes.html", {"products": products})


def product_description(request, id):
    product = AdmProducts.objects.get(id=id)
    return render(request, "user/product_description.html", {"product": product})


def add_to_cart(request, id):
    user = request.user
    product = AdmProducts.objects.get(id=id)

    cart, created = Cart.objects.get_or_create(user=user)

    try:
        cart_item = Cartitem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
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
    final_total = 0

    for item in cart_items:
        item.offer_price = item.product.productvariant_set.first().offer_price
        item.total_price_each = item.offer_price * item.quantity
        total_price += item.total_price_each

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
    addresses = Address.objects.filter(user=user)
    cart_items_param = request.GET.get("cart_items")

    selected_address_id = None
    order = None

    if request.method == "POST":
        cart = Cart.objects.get(user=user)
        cart_items = Cartitem.objects.filter(cart=cart)
        selected_address_id = request.POST.get("selected_address")

        if selected_address_id:
            address = Address.objects.get(id=selected_address_id)
            payment_method = "Cash On Delivery"

            total_price = 0

            for item in cart_items:
                item.offer_price = item.product.productvariant_set.first().offer_price
                item.total_price_each = item.offer_price * item.quantity
                print(item.total_price_each)

                total_price += item.total_price_each

            total_price_shipping = total_price + 1000

            order = Order.objects.create(
                user=user,
                address=address,
                payment_method=payment_method,
                total_price=total_price,
                total_price_shipping=total_price_shipping,
            )

            for item in cart_items:
                product = item.product
                quantity = item.quantity

                product_variant = product.productvariant_set.first()

                if product_variant.stock >= quantity:
                    product_variant.stock -= quantity
                    product_variant.save()

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                else:
                    pass

            cart_items.delete()

            return redirect(
                "order_summary", address_id=selected_address_id, order_id=order.id
            )

    if cart_items_param == "true":
        cart = Cart.objects.get(user=user)
        cart_items = Cartitem.objects.filter(cart=cart)

        total_price = 0
        for item in cart_items:
            item.offer_price = item.product.productvariant_set.first().offer_price
            item.total_price_each = item.offer_price * item.quantity
            total_price += item.total_price_each

        final_total = total_price + 1000

        return render(
            request,
            "user/checkout.html",
            {
                "addresses": addresses,
                "cart_items": cart_items,
                "total_price": total_price,
                "final_total": final_total,
                "address_id": selected_address_id,
            },
        )

    return render(
        request,
        "user/checkout.html",
        {"addresses": addresses, "address_id": selected_address_id},
    )


def add_checkout_address(request):
    if request.method == "POST":
        # Extract data from the form
        housename_companyname = request.POST.get("Housename_companyname")
        post_office = request.POST.get("Post_office")
        street = request.POST.get("Street")
        city = request.POST.get("City")
        state = request.POST.get("State")
        country = request.POST.get("Country")
        pin_code = request.POST.get("Pin_code")

        # Create a new Address object
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


def order_summary(request, address_id, order_id):
    user = request.user
    address = Address.objects.get(id=address_id)
    username = user.username

    orders = Order.objects.filter(id=order_id, address=address)
    order_items = OrderItem.objects.filter(order=order_id)

    context = {
        "address": address,
        "username": username,
        "orders": orders,
        "order_items": order_items,
    }

    return render(request, "user/order_summary.html", context)

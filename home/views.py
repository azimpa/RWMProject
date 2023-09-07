from django.shortcuts import render, redirect, get_object_or_404
from home.models import Address
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from adm.models import (
    AdmProducts,
    AdmCategories,
    ProductVariant,
    ProductColor,
    ProductSize,
)
from home.models import Cartitem, Cart, Order, OrderItem

# Create your views here.


def home(request):
    products = AdmProducts.objects.filter(is_active=True).order_by("id")

    if request.user.is_anonymous:
        return render(request, "user/home.html", {"products": products})
    elif request.user.is_superuser:
        logout(request)
        return render(request, "user/home.html", {"products": products})
    else:
        products = AdmProducts.objects.filter(is_active=True).order_by("id")
        return render(request, "user/home.html", {"products": products})


def useraddress(request):
    if not request.user.is_authenticated:
        return redirect("user_login")

    user = request.user
    address = Address.objects.filter(user=user)
    return render(request, "user/useraddress.html", {"addresses": address})


def add_address(request):
    if not request.user.is_authenticated:
        return redirect("user_login")

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
    if not request.user.is_authenticated:
        return redirect("user_login")

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
    products = AdmProducts.objects.filter(is_active=True).order_by("id")
    variants = (
        ProductVariant.objects.filter(product__in=products, is_active=True)
        .order_by("product", "id")
        .distinct("product")
    )
    return render(
        request,
        "user/total_products.html",
        {"products": products, "variants": variants},
    )


def roadbikes(request):
    category = AdmCategories.objects.get(name="road_bikes", is_active=True)
    products = AdmProducts.objects.filter(category=category, is_active=True)
    return render(request, "user/roadbikes.html", {"products": products})


def gravelbikes(request):
    category = AdmCategories.objects.get(name="gravel_bikes", is_active=True)
    products = AdmProducts.objects.filter(category=category, is_active=True)
    return render(request, "user/gravelbikes.html", {"products": products})


def hybridbikes(request):
    category = AdmCategories.objects.get(name="hybrid_bikes", is_active=True)
    products = AdmProducts.objects.filter(category=category, is_active=True)
    return render(request, "user/hybridbikes.html", {"products": products})


def mountainbikes(request):
    category = AdmCategories.objects.get(name="mountain_bikes", is_active=True)
    products = AdmProducts.objects.filter(category=category, is_active=True)
    return render(request, "user/mountainbikes.html", {"products": products})


def product_description(request, id):
    var = ProductVariant.objects.get(id=id)
    variants = ProductVariant.objects.filter(product=var.product, is_active=True)

    colors = variants.values_list("color", flat=True).distinct()
    sizes = variants.values_list("size", flat=True).distinct()

    available_colors = ProductColor.objects.filter(id__in=colors, is_active=True)
    available_sizes = ProductSize.objects.filter(id__in=sizes, is_active=True)

    selected_color_id = request.GET.get("selected_color")
    selected_size_id = request.GET.get("selected_size")

    if selected_color_id:
        variants = variants.filter(color_id=selected_color_id)

    if selected_size_id:
        variants = variants.filter(size_id=selected_size_id)

    # Create a list of dictionaries containing variant data, including color image URLs
    variants_data = []
    for variant in variants:
        color_images = variant.images.all()  # Get all associated VariantImage objects
        color_image_urls = [
            image.image.url for image in color_images
        ]  # Get URLs for each image
        color = ProductColor.objects.get(id=variant.color_id)
        color_name = color.name
        size = ProductSize.objects.get(id=variant.size_id)
        size_name = size.name
        variants_data.append(
            {
                "id": variant.id,
                "color_id": variant.color_id,
                "size_id": variant.size_id,
                "size_name": size_name,
                "color_name": color_name,
                "price": str(variant.price),
                "offer_price": str(variant.offer_price),
                "discount": str(variant.discount),
                "stock": variant.stock,
                "is_available": variant.is_available,
                "is_active": variant.is_active,
                "color_image_urls": color_image_urls,  # Add the list of color image URLs
            }
        )

    # Create a dictionary with the data you want to send back
    response_data = {
        "products": {
            "name": var.product.name,
            # Add other product details here
        },
        "variants": variants_data,  # Use the list of dictionaries
    }

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # If it's an AJAX request, return JSON response
        return JsonResponse(response_data)

    # If it's not an AJAX request, render the HTML template
    return render(
        request,
        "user/product_description.html",
        {
            "products": var,
            "variants": variants,
            "colors": available_colors,
            "sizes": available_sizes,
        },
    )


def add_to_cart(request, id):
    if not request.user.is_authenticated:
        return redirect("user_login")

    user = request.user

    try:
        product_variant = ProductVariant.objects.get(id=id)

        if product_variant.stock > 0:
            cart, created = Cart.objects.get_or_create(user=user)

            try:
                cart_item = Cartitem.objects.get(cart=cart, product=product_variant)
                cart_item.quantity += 1
                cart_item.save()
                messages.success(
                    request, f"{product_variant.product} quantity updated in your cart."
                )
            except Cartitem.DoesNotExist:
                cart_item = Cartitem(cart=cart, product=product_variant)
                cart_item.save()
                messages.success(
                    request, f"{product_variant.product} added to your cart."
                )
        else:
            messages.error(request, f"{product_variant.product} is out of stock.")
    except ProductVariant.DoesNotExist:
        messages.error(request, f"Product variant not available.")

    return redirect("cart")


def cart(request):
    if not request.user.is_authenticated:
        return redirect("user_login")

    user = request.user
    cart_items = Cartitem.objects.filter(cart__user=user)

    total_price = 0
    final_total = 0

    for item in cart_items:
        item.offer_price = item.product.offer_price
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
            if cart_item.quantity < cart_item.product.stock:
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
            request, f"{cart_item.product} has been removed from your cart."
        )
    except Cartitem.DoesNotExist:
        messages.error(request, "Cart item not found.")

    return redirect("cart")


def checkout(request):
    if not request.user.is_authenticated:
        return redirect("user_login")

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
                item.offer_price = item.product.offer_price
                item.total_price_each = item.offer_price * item.quantity

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
                product_variant = product

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
            item.offer_price = item.product.offer_price
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
    if not request.user.is_authenticated:
        return redirect("user_login")

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
    if not request.user.is_authenticated:
        return redirect("user_login")

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
    if not request.user.is_authenticated:
        return redirect("user_login")

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


def my_orders(request):
    if not request.user.is_authenticated:
        return redirect("user_login")

    user = request.user
    orders = Order.objects.filter(user=user)

    order_items = OrderItem.objects.filter(order__in=orders).order_by("-id")

    return render(request, "user/my_orders.html", {"order_items": order_items})


def cancel_order(request, order_id, product_id):
    order = get_object_or_404(Order, id=order_id)
    order_item = OrderItem.objects.filter(order=order, product_id=product_id).first()

    if order_item:
        order_item.order_status = "Cancelled"
        order_item.save()

    return redirect("my_orders")

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import CustomUser
from django.http import JsonResponse
from home.models import Order, OrderItem
from adm.models import (
    AdmCategories,
    AdmProducts,
    ProductSize,
    ProductColor,
    ProductVariant,
    VariantImage,
)


def index(request):
    if request.user.is_anonymous:
        return render(request, "adm/index.html")
    elif not request.user.is_superuser:
        logout(request)
        return render(request, "adm/index.html")
    else:
        return render(request, "adm/index.html")


def adm_login(request):
    if request.method == "POST":
        admname = request.POST["username"]
        admpass = request.POST["password"]
        super_user = authenticate(request, username=admname, password=admpass)
        if super_user is not None and super_user.is_superuser:
            login(request, super_user)
            return redirect("index")
        else:
            messages.warning(request, "Not a Super User")
            return redirect("adm_login")
    return render(request, "adm/adm_login.html")


def adm_logout(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    logout(request)
    return redirect("index")


def user_details(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    adm_users = CustomUser.objects.all().order_by("id")
    return render(request, "adm/user_details.html", {"admin_users": adm_users})


def Admin_block_user(request, id):
    adm_users = CustomUser.objects.get(id=id)
    adm_users.is_active = False
    adm_users.save()
    return redirect("user_details")


def Admin_unblock_user(request, id):
    ad_users = CustomUser.objects.get(id=id)
    ad_users.is_active = True
    ad_users.save()
    return redirect("user_details")


def adm_categories(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    category = AdmCategories.objects.all().order_by("id")
    return render(request, "adm/adm_categories.html", {"categories": category})


def add_adm_categories(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    if request.method == "POST":
        cat_name = request.POST.get("category_name", "")

        if cat_name.strip():
            if AdmCategories.objects.filter(name=cat_name).exists():
                messages.error(request, f'The category "{cat_name}" already exists.')
                return redirect("add_adm_categories")

            category = AdmCategories(name=cat_name)
            category.save()
            return redirect("adm_categories")
        else:
            messages.error(request, "Category name cannot be empty.")
            return redirect("add_adm_categories")

    return render(request, "adm/add_adm_categories.html")


def edit_adm_categories(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    category = get_object_or_404(AdmCategories, id=id)

    if request.method == "POST":
        new_name = request.POST.get("edited_category_name", "")
        if new_name:
            category.name = new_name
            category.save()
            return redirect("adm_categories")
    return render(request, "adm/edit_adm_categories.html", {"cat": category})


def delete_adm_categories(request, id):
    category = get_object_or_404(AdmCategories, id=id)
    category.delete()
    return redirect("adm_categories")


def adm_product(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    adm_products = AdmProducts.objects.all().order_by("id")
    return render(request, "adm/adm_product.html", {"products": adm_products})


def add_adm_product(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    if request.method == "POST":
        prod_name = request.POST.get("product_name", "")
        prod_brand = request.POST.get("product_brand", "")
        category = request.POST.get("product_categories", "")
        image = request.FILES.get("product_images")
        cat = AdmCategories.objects.get(id=category)
        product_description = request.POST.get("product_description")
        prod_status = request.POST.get("product_status", "active")

        if AdmProducts.objects.filter(name=prod_name).exists():
            messages.error(request, f'The product "{prod_name}" already exists.')
            return redirect("add_adm_product")

        product = AdmProducts(
            name=prod_name,
            brand=prod_brand,
            images=image,
            category=cat,
            status=prod_status,
            description=product_description,
        )
        product.save()
        return redirect("adm_product")

    else:
        categories = AdmCategories.objects.all()
        return render(request, "adm/add_adm_product.html", {"categories": categories})


def edit_adm_product(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product = get_object_or_404(AdmProducts, id=id)

    if request.method == "POST":
        edited_name = request.POST.get("edited_product_name", "")
        edited_brand = request.POST.get("edited_brand", "")
        edited_image = request.FILES.get("edited_existing_image")
        edited_category = request.POST.get("edited_category", "")
        editcat = AdmCategories.objects.get(id=edited_category)
        edited_description = request.POST.get("edited_description")
        edited_status = request.POST.get("edited_status", "active")

        product.name = edited_name
        product.images = edited_image
        product.brand = edited_brand
        product.category = editcat
        product.description = edited_description
        product.status = edited_status
        product.save()

        return redirect("adm_product")

    else:
        categories = AdmCategories.objects.all()
        return render(
            request,
            "adm/edit_adm_product.html",
            {
                "product": product,
                "categories": categories,
            },
        )


def delete_adm_product(request, id):
    product = get_object_or_404(AdmProducts, id=id)
    product.delete()
    return redirect("adm_product")


def product_color(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product_color = ProductColor.objects.all().order_by("id")
    return render(request, "adm/product_color.html", {"product_color": product_color})


def add_product_color(request):
    if not request.user.is_authenticated:
        return redirect("adm_login")

    product_color = ProductColor.objects.all()

    if request.method == "POST":
        color_name = request.POST.get("name", "")

        if color_name.strip():
            if ProductColor.objects.filter(name=color_name).exists():
                messages.error(request, f'The color "{color_name}" already exists.')
                return render(
                    request,
                    "adm/add_product_color.html",
                    {"product_color": product_color},
                )

            else:
                color = ProductColor(name=color_name)
                color.save()
                messages.success(
                    request, f'The color "{color_name}" was added successfully.'
                )
                return redirect("product_color")
        else:
            messages.error(request, "Color name cannot be empty.")
            return redirect("add_product_color")

    return render(
        request, "adm/add_product_color.html", {"product_color": product_color}
    )


def edit_product_color(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product_color = get_object_or_404(ProductColor, id=id)

    if request.method == "POST":
        new_name = request.POST.get("edited_color", "")
        if new_name.strip():
            product_color.name = new_name
            product_color.save()
            return redirect("product_color")
        else:
            messages.error(request, "Color name cannot be empty.")

    return render(
        request, "adm/edit_product_color.html", {"product_color": product_color}
    )


def delete_product_color(request, id):
    product_color = get_object_or_404(ProductColor, id=id)
    product_color.delete()
    return redirect("product_color")


def product_size(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product_size = ProductSize.objects.all().order_by("id")
    return render(request, "adm/product_size.html", {"product_size": product_size})


def add_product_size(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product_size = ProductSize.objects.all()

    if request.method == "POST":
        size_name = request.POST.get("name", "")

        if size_name.strip():
            if ProductSize.objects.filter(name=size_name).exists():
                messages.error(request, f'The size "{size_name}" already exists.')
                return render(
                    request, "adm/add_product_size.html", {"product_size": product_size}
                )

            else:
                size = ProductSize(name=size_name)
                size.save()
                messages.success(
                    request, f'The size "{size_name}" was added successfully.'
                )
                return redirect("product_size")
        else:
            messages.error(request, "size name cannot be empty.")
            return redirect("add_product_size")

    return render(request, "adm/add_product_size.html", {"product_size": product_size})


def edit_product_size(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product_size = get_object_or_404(ProductSize, id=id)

    if request.method == "POST":
        new_name = request.POST.get("edited_size", "")
        if new_name.strip():
            product_size.name = new_name
            product_size.save()
            return redirect("product_size")
        else:
            messages.error(request, "size name cannot be empty.")

    return render(request, "adm/edit_product_size.html", {"product_size": product_size})


def delete_product_size(request, id):
    product_size = get_object_or_404(ProductSize, id=id)
    product_size.delete()
    return redirect("product_size")


def product_variant(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    try:
        product = AdmProducts.objects.get(id=id)
        variants = ProductVariant.objects.filter(product=product)

        if variants.exists():
            variants = variants.order_by("id")
            return render(
                request,
                "adm/product_variant.html",
                {"variants": variants, "product": product},
            )
        else:
            messages.error(request, "No variants found for this product")
            return render(
                request,
                "adm/product_variant.html",
                {"variants": variants, "product": product},
            )
    except AdmProducts.DoesNotExist:
        messages.error(request, "Product not found")
        return redirect("adm_product")


def add_product_variant(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    if request.method == "POST":
        try:
            product = AdmProducts.objects.get(id=id)
            variant_color = request.POST.get("color")
            color = ProductColor.objects.get(id=variant_color)
            variant_size = request.POST.get("size")
            size = ProductSize.objects.get(id=variant_size)
            variant_price = request.POST.get("price")
            variant_offer_price = request.POST.get("offer_price")
            variant_discount = request.POST.get("discount")
            variant_stock = request.POST.get("stock")
            variant_is_available = request.POST.get("is_available")

            variant_images = request.FILES.getlist("images")

            variant = ProductVariant.objects.create(
                product=product,
                color=color,
                size=size,
                price=variant_price,
                offer_price=variant_offer_price,
                discount=variant_discount,
                stock=variant_stock,
                is_available=variant_is_available,
            )

            for image in variant_images:
                variant.images.create(image=image)

            messages.success(request, "Product variant added successfully")
            return redirect("product_variant", id=product.id)

        except (ProductColor.DoesNotExist, ProductSize.DoesNotExist):
            messages.error(request, "Invalid color or size selection")
            return redirect("add_product_variant", id=id)

        except Exception as e:
            messages.error(
                request, "An error occurred while adding the product variant"
            )
            return redirect("add_product_variant", id=id)

    else:
        product = AdmProducts.objects.get(id=id)
        colors = ProductColor.objects.all()
        sizes = ProductSize.objects.all()

        return render(
            request,
            "adm/add_product_variant.html",
            {"product": product, "colors": colors, "sizes": sizes},
        )


def edit_product_variant(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    try:
        variant = ProductVariant.objects.get(id=id)
    except ProductVariant.DoesNotExist:
        messages.error(request, "Variant not found")
        return redirect("adm_product")

    if request.method == "POST":
        try:
            edited_color_id = request.POST.get("edited_color")
            edited_size_id = request.POST.get("edited_size")
            edited_price = request.POST.get("edited_price")
            edited_offer_price = request.POST.get("edited_offer_price")
            edited_discount = request.POST.get("edited_discount")
            edited_stock = request.POST.get("edited_stock")
            edited_is_available = request.POST.get("edited_is_available")

            edited_color = ProductColor.objects.get(pk=edited_color_id)
            edited_size = ProductSize.objects.get(pk=edited_size_id)

            variant.color = edited_color
            variant.size = edited_size
            variant.price = edited_price
            variant.offer_price = edited_offer_price
            variant.discount = edited_discount
            variant.stock = edited_stock
            variant.is_available = edited_is_available
            variant.save()

            selected_image_id = request.POST.get("selected_image")

            new_image = request.FILES.get("new_images")

            removed_image_id = request.POST.get("selected_image")

            if selected_image_id and new_image:
                try:
                    selected = VariantImage.objects.get(id=selected_image_id)
                    selected.image.delete()  # Delete the old image
                    selected.image = new_image
                    selected.save()
                except VariantImage.DoesNotExist:
                    pass

            # Handling deletion of images
            elif removed_image_id:
                try:
                    image = VariantImage.objects.get(id=removed_image_id)
                    image.image.delete()
                    image.delete()
                    messages.success(request, "Image removed successfully")
                except VariantImage.DoesNotExist:
                    messages.error(request, "Failed to remove image")

            # Handling addition of new images
            new_variant_images = request.FILES.getlist("images")
            if new_variant_images:
                for image in new_variant_images:
                    if image:
                        variant.images.create(image=image)

            messages.success(request, "Product variant updated successfully")
            product_id = variant.product.id
            return redirect("product_variant", id=product_id)

        except (ProductColor.DoesNotExist, ProductSize.DoesNotExist):
            messages.error(request, "Invalid color or size selection")
        except Exception as e:
            messages.error(
                request, "An error occurred while updating the product variant"
            )

    colors = ProductColor.objects.all()
    sizes = ProductSize.objects.all()

    return render(
        request,
        "adm/edit_product_variant.html",
        {
            "variants": variant,
            "colors": colors,
            "sizes": sizes,
            "selected_color": variant.color,
            "selected_size": variant.size,
        },
    )


def delete_product_variant(request, id):
    product_variant = get_object_or_404(ProductVariant, id=id)
    product_id = product_variant.product.id
    product_variant.delete()
    return redirect("product_variant", id=product_id)


def adm_order(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    users = CustomUser.objects.filter(is_superuser=False)
    orders = Order.objects.filter(user__in=users).order_by("id")

    return render(request, "adm/adm_order.html", {"orders": orders})


def adm_order_items(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    order_items = OrderItem.objects.filter(order_id=id).order_by("id")

    return render(request, "adm/adm_order_items.html", {"order_items": order_items})


def edit_order_status(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    order_items = get_object_or_404(OrderItem, id=id)

    if request.method == "POST":
        order_status = request.POST.get("edited_order_status", "")
        if order_status:
            order_items.order_status = order_status
            order_items.save()
            return redirect("adm_order")

    return render(request, "adm/edit_order_status.html", {"order_items": order_items})

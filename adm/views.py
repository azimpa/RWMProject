from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import CustomUser
from adm.models import AdmCategories, AdmProducts, ProductSize, ProductColor, ProductVariant


def index(request):
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
    print(adm_users)
    return render(request, "adm/user_details.html", {"admin_users": adm_users})

def Admin_block_user(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    adm_users = CustomUser.objects.get(id=id)
    adm_users.is_active = False
    adm_users.save()
    return redirect("user_details")

def Admin_unblock_user(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

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
                messages.error(
                    request, f'The category "{cat_name}" already exists.')
                return redirect("add_adm_categories")

            category = AdmCategories(name=cat_name)
            category.save()
            print("New category saved:", category.name)
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
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")
    
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
        prod_image = request.FILES.get("product_image", None)
        prod_brand = request.POST.get("product_brand", "")
        category = request.POST.get("product_categories", "")
        cat = AdmCategories.objects.get(id=category)
        prod_status = request.POST.get("product_status", "active")

        if AdmProducts.objects.filter(name=prod_name).exists():
            messages.error(
                request, f'The product "{prod_name}" already exists.')
            return redirect("add_adm_product")

        product = AdmProducts(
            name=prod_name,
            brand=prod_brand,
            category=cat,
            product_image=prod_image,
            status=prod_status,
        )
        product.save()
        return redirect("adm_product")
    
    else:
        categories = AdmCategories.objects.all()
        return render(request, "adm/add_adm_product.html", {'categories': categories})

def edit_adm_product(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product = get_object_or_404(AdmProducts, id=id)

    if request.method == "POST":
        edited_name = request.POST.get("edited_product_name", "")
        edited_image = request.FILES.get("edited_product_image", None)
        edited_brand = request.POST.get("edited_brand", "")
        edited_category = request.POST.get("edited_category", "")
        editcat = AdmCategories.objects.get(id=edited_category)
        edited_status = request.POST.get("edited_status", "active")

        product.name = edited_name
        product.brand = edited_brand
        product.category = editcat
        product.product_image = edited_image
        product.status = edited_status

        product.save()

        return redirect("adm_product")

    else:
        categories = AdmCategories.objects.all()
        return render(request, "adm/edit_adm_product.html", {'product': product, 'categories': categories,})

def delete_adm_product(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product = get_object_or_404(AdmProducts, id=id)
    product.delete()
    return redirect("adm_product")

def adm_order(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")
    
    return render(request, "adm/adm_order.html")

def product_color(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product_color = ProductColor.objects.all().order_by("id")
    return render(request, "adm/product_color.html", {'product_color': product_color})

def add_product_color(request):
    if not request.user.is_authenticated:
        return redirect("adm_login")

    product_color = ProductColor.objects.all()

    if request.method == "POST":
        color_name = request.POST.get("name", "")

        if color_name.strip():
            if ProductColor.objects.filter(name=color_name).exists():
                messages.error(
                    request, f'The color "{color_name}" already exists.')
                return render(request, "adm/add_product_color.html", {'product_color': product_color})

            else:
                color = ProductColor(name=color_name)
                color.save()
                print("New color saved:", color.name)
                messages.success(
                    request, f'The color "{color_name}" was added successfully.')
                return redirect("product_color")
        else:
            messages.error(request, "Color name cannot be empty.")
            return redirect("add_product_color")

    return render(request, "adm/add_product_color.html", {'product_color': product_color})

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

    return render(request, "adm/edit_product_color.html", {"product_color": product_color})

def delete_product_color(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product_color = get_object_or_404(ProductColor, id=id)
    product_color.delete()
    return redirect("product_color")

def product_size(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product_size = ProductSize.objects.all().order_by("id")
    return render(request, "adm/product_size.html", {'product_size': product_size})

def add_product_size(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product_size = ProductSize.objects.all()

    if request.method == "POST":
        size_name = request.POST.get("name", "")

        if size_name.strip():
            if ProductSize.objects.filter(name=size_name).exists():
                messages.error(
                    request, f'The size "{size_name}" already exists.')
                return render(request, "adm/add_product_size.html", {'product_size': product_size})

            else:
                size = ProductSize(name=size_name)
                size.save()
                print("New size saved:", size.name)
                messages.success(
                    request, f'The size "{size_name}" was added successfully.')
                return redirect("product_size")
        else:
            messages.error(request, "size name cannot be empty.")
            return redirect("add_product_size")

    return render(request, "adm/add_product_size.html", {'product_size': product_size})

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
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product_size = get_object_or_404(ProductSize, id=id)
    product_size.delete()
    return redirect("product_size")





def product_variant(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    variant = ProductVariant.objects.all().order_by("id")
    return render(request, "adm/product_variant.html", {"variants": variant})

def add_product_variant(request, product_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")
    
    if request.method == 'POST':
        product = AdmProducts.objects.get(pk=product_id)

        color_id = request.POST.get('color')
        size_id = request.POST.get('size')
        price = request.POST.get('price')
        offer_price = request.POST.get('offer_price')
        stock = request.POST.get('stock')
        discount = request.POST.get('discount')
        status = request.POST.get('status')

        try:
            color = ProductColor.objects.get(pk=color_id)
            size = ProductSize.objects.get(pk=size_id)
            
            variant = ProductVariant.objects.create(
                product=product,
                color=color,
                size=size,
                price=price,
                offer_price=offer_price,
                stock=stock,
                discount=discount,
                status=status
            )

            messages.success(request, 'Product variant added successfully')
            return redirect('adm_product') 
        except (ProductColor.DoesNotExist, ProductSize.DoesNotExist):
            messages.error(request, 'Invalid color or size selection')
            return render(request, 'add_product_variant.html')
        except Exception as e:
            error_message = str(e)
            return render(request, 'add_product_variant.html')
    else:
        product = AdmProducts.objects.get(pk=product_id)
        colors = ProductColor.objects.all()
        sizes = ProductSize.objects.all()

        return render(request, 'add_product_variant.html', {'product': product, 'colors': colors, 'sizes': sizes})

def edit_product_variant(request, variant_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    try:
        variant = ProductVariant.objects.get(pk=variant_id)
    except ProductVariant.DoesNotExist:
        messages.error(request, 'Variant not found')
        return redirect('adm_product')  
    
    if request.method == 'POST':
        color_id = request.POST.get('edited_colors')
        size_id = request.POST.get('edited_sizes')
        price = request.POST.get('edited_price')
        offer_price = request.POST.get('edited_offer_price')
        stock = request.POST.get('edited_stock')
        discount = request.POST.get('edited_discount')
        status = request.POST.get('edited_status')

        try:
            color = ProductColor.objects.get(pk=color_id)
            size = ProductSize.objects.get(pk=size_id)
            
            variant.color = color
            variant.size = size
            variant.price = price
            variant.offer_price = offer_price
            variant.stock = stock
            variant.discount = discount
            variant.status = status
            variant.save()

            messages.success(request, 'Product variant updated successfully')
            return redirect('adm_product') 
        except (ProductColor.DoesNotExist, ProductSize.DoesNotExist):
            messages.error(request, 'Invalid color or size selection')
            return render(request, 'edit_product_variant.html', {'variant': variant})
        except Exception as e:
            error_message = str(e)
            return render(request, 'edit_product_variant.html', {'variant': variant})
    else:
        colors = ProductColor.objects.all()
        sizes = ProductSize.objects.all()

        return render(request, 'edit_product_variant.html', {'variant': variant, 'colors': colors, 'sizes': sizes})
    
def delete_product_variant(request, variant_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("adm_login")

    product_variant = get_object_or_404(ProductVariant, id=variant_id)
    product_variant.delete()
    return redirect("product_variant")
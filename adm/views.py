from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import CustomUser
from adm.models import AdmCategories, AdmProducts

def baseadmin(request):
    return render(request, 'adm/base.html')

def index(request):
    return render(request, 'adm/index.html')

def adm_login(request):
    if request.method == 'POST':
        admname = request.POST['username']
        admpass = request.POST['password']
        super_user = authenticate(request, username=admname, password=admpass)
        if super_user is not None and super_user.is_superuser:
            login(request, super_user)
            return redirect('index')
        else:
            messages.warning(request, "Not a Super User")
            return redirect('adm_login')
    return render(request, 'adm/adm_login.html')

def adm_logout(request):
    logout(request)
    return redirect('index')

def user_details(request):
    adm_users = CustomUser.objects.all().order_by('id')
    print(adm_users)
    return render(request, 'adm/user_details.html', {'admin_users': adm_users})

def Admin_block_user(request, id):
    adm_users = CustomUser.objects.get(id=id)
    adm_users.is_active = False
    adm_users.save()
    return redirect('user_details')

def Admin_unblock_user(request, id):
    ad_users = CustomUser.objects.get(id=id)
    ad_users.is_active = True
    ad_users.save()
    return redirect('user_details')

def adm_categories(request):
    adm_category = AdmCategories.objects.all()
    return render(request, 'adm/adm_categories.html', {'categories': adm_category})

def add_adm_categories(request):
    if request.method == 'POST':
        cat_name = request.POST.get('category_name', '') 
        if cat_name is not None:
            category = AdmCategories(name=cat_name)
            category.save()
            return redirect('adm_categories')
    return render(request, 'adm/add_adm_categories.html')

def edit_adm_categories(request, id):
    category = get_object_or_404(AdmCategories, id=id)

    if request.method == 'POST':
        new_name = request.POST.get('edited_category_name', '') 
        if new_name:
            category.name = new_name
            category.save()
            return redirect('adm_categories')
    return render(request, 'adm/edit_adm_categories.html', {'cat': category})

def delete_adm_categories(request, id):
    category = get_object_or_404(AdmCategories, id=id)
    category.delete()
    return redirect('adm_categories')

def adm_product(request):
    adm_products = AdmProducts.objects.all()
    return render(request, 'adm/adm_product.html', {'products': adm_products})

def add_adm_product(request):
    if request.method == 'POST':
        prod_name = request.POST.get('product_name', '')
        prod_brand = request.POST.get('brand', '')
        prod_category = request.POST.get('category', '')
        prod_image = request.FILES.get('product_image', None)
        prod_size = request.POST.get('size', '')
        prod_color = request.POST.get('color', '')
        prod_price = request.POST.get('price', '')
        prod_offer_price = request.POST.get('offer_price', '')
        prod_quantity = request.POST.get('quantity', '')
        prod_discount = request.POST.get('discount', '')
        prod_status = request.POST.get('status', 'active')

        product = AdmProducts(
            name=prod_name,
            brand=prod_brand,
            category=prod_category,
            product_image=prod_image,
            size=prod_size,
            color=prod_color,
            price=prod_price,
            offer_price=prod_offer_price,
            quantity=prod_quantity,
            discount=prod_discount,
            status=prod_status
        )

        product.save()
        return redirect('adm_product')

    return render(request, 'adm/add_adm_product.html')

def edit_adm_product(request, id):
    product = get_object_or_404(AdmProducts, id=id)

    if request.method == 'POST':
        edited_name = request.POST.get('edited_product_name', '')
        edited_brand = request.POST.get('edited_brand', '')
        edited_category = request.POST.get('edited_category', '')
        edited_image = request.FILES.get('edited_product_image', None)
        edited_size = request.POST.get('edited_size', '')
        edited_color = request.POST.get('edited_color', '')
        edited_price = request.POST.get('edited_price', '')
        edited_offer_price = request.POST.get('edited_offer_price', '')
        edited_quantity = request.POST.get('edited_quantity', '')
        edited_discount = request.POST.get('edited_discount', '')
        edited_status = request.POST.get('edited_status', 'active')

        if edited_name:
            product.name = edited_name
        if edited_brand:
            product.brand = edited_brand
        if edited_category:
            product.category = edited_category
        if edited_image:
            product.product_image = edited_image
        if edited_size:
            product.size = edited_size
        if edited_color:
            product.color = edited_color
        if edited_price:
            product.price = edited_price
        if edited_offer_price:
            product.offer_price = edited_offer_price
        if edited_quantity:
            product.quantity = edited_quantity
        if edited_discount:
            product.discount = edited_discount
        if edited_status:
            product.status = edited_status

        product.save()
        return redirect('adm_product') 

    return render(request, 'adm/edit_adm_product.html', {'product': product})


def delete_adm_product(request,id):
    product = get_object_or_404(AdmProducts, id=id)
    product.delete()
    return redirect('adm_product')


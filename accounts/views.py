from django.shortcuts import render, redirect,get_object_or_404
from .models import CustomUser
from django.contrib import messages
from django.contrib import auth
from django.views.decorators.cache import never_cache
from . import verify

# Create your views here.


@never_cache
def signup(request):
    if request.method == "POST":
        user_name = request.POST["username"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        pass1 = request.POST["password1"]
        pass2 = request.POST["password2"]

        print(f"username: {user_name}\n email: {email}\n pass1: {pass1}\n pass2: {pass2}\n phone:{phone_number}")

        if pass1 != pass2:
            return redirect(signup)

        if len(phone_number) < 10 or len(phone_number) > 14:
            return redirect(signup)
        
        if len(pass1) <2:
              return redirect(signup)
        
        try:
            if CustomUser.objects.get(username=user_name):
                return redirect(signup)
        except:
            pass

        try:
            if CustomUser.objects.get(email=email):
                return redirect(signup)
        except:
            pass

        try:
            if CustomUser.objects.get(phone_number=phone_number):
                return redirect(signup)
        except:
            pass

        my_user = CustomUser.objects.create(
            username=user_name,
            email=email,
            phone_number=phone_number)
        
        my_user.set_password(pass1)
        my_user.save()

        auth.login(request, my_user)
        verify.send(my_user.phone_number)
        return redirect('otpcheck',phone_number,my_user.id)
    
    return render(request, "auth/signup.html")

@never_cache
def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method=='POST':
        email=request.POST['email']
        pass1=request.POST['pass']

        try:
            user = CustomUser.objects.get(email=email)
            password_matched = user.check_password(pass1)

            print(user.email,user.password,pass1)

        except:
            print(email,pass1)
            messages.error(request, 'Incorrect entry')
            return redirect('login')   
        
        if user and password_matched:
            auth.login(request, user) 
            return redirect('home') 
        
    return render(request, 'auth/login.html')

@never_cache
def otpcheck(request, id, phone_number):
    user = get_object_or_404(CustomUser, id=id)

    if request.method == 'POST':
        code = request.POST.get("otp")

        if verify.check(phone_number, code):
            user.is_verified = True
            user.save()
            return redirect('login')
        else:
            user.delete()
            return redirect('signup')
    else:
        return render(request, 'auth/otpcheck.html', {'phone_number': phone_number, 'id': id})

@never_cache
def logout(request):
    auth.logout(request)
    return redirect('home')    

@never_cache
def userprofile(request):
    username = request.user.username
    return render(request,'user/userprofile.html',{'username': username})    
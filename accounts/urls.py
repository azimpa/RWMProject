from django.urls import path
from accounts import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("otpcheck/<str:phone_number>,<int:id>", views.otpcheck, name="otpcheck"),
    path("logout", views.logout, name="logout"),
    path("userprofile", views.userprofile, name="userprofile"),
    path("forgot_password", views.forgot_password, name="forgot_password"),
    path("forgot_otpcheck/<str:phone_number>,<int:id>", views.forgot_otpcheck, name="forgot_otpcheck"),
]

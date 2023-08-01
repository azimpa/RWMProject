from django.urls import path
from accounts import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('otpcheck/<str:phone_number>,<int:id>', views.otpcheck, name='otpcheck'),
    path('logout', views.logout, name='logout'),
    path('userprofile', views.userprofile, name='userprofile'),
]

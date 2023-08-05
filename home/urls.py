from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('product', views.product, name="product"),
    path('base_user', views.base_user, name="base_user"),
]    
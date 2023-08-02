from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('categories', views.categories, name="categories"),
    path('product', views.product, name="product"),
    path('contact', views.contact, name="contact"),
]

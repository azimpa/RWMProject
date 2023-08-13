from django.urls import path
from home import views

urlpatterns = [
    path("", views.home, name="home"),
    path("useraddress", views.useraddress, name="useraddress"),
    path("add_address", views.add_address, name="add_address"),
    path('delete_address/<int:id>', views.delete_address, name='delete_address'),
    path('edit_address/<int:id>', views.edit_address, name='edit_address'),
    path('total_products', views.total_products, name='total_products'),
    path('roadbikes', views.roadbikes, name='roadbikes'),
    path('gravelbikes', views.gravelbikes, name='gravelbikes'),
    path('hybridbikes', views.hybridbikes, name='hybridbikes'),
    path('mountainbikes', views.mountainbikes, name='mountainbikes'),
    path('product_description/<int:id>', views.product_description, name="product_description"),  
    path('cart', views.cart, name="cart"), 
    path('checkout', views.checkout, name="checkout"), 
]

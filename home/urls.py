from django.urls import path
from home import views

urlpatterns = [
    path("", views.home, name="home"),
    path("product", views.product, name="product"),
    path("useraddress", views.useraddress, name="useraddress"),
    path("add_address", views.add_address, name="add_address"),
    path('delete_address/<int:id>', views.delete_address, name='delete_address'),
    path('edit_address/<int:id>', views.edit_address, name='edit_address'),
]

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
    path('add_to_cart/<int:id>', views.add_to_cart, name="add_to_cart"), 
    path('cart', views.cart, name="cart"),
    path('update_cart_item/<int:id>', views.update_cart_item, name="update_cart_item"),
    path('clear_cart_item', views.clear_cart_item, name="clear_cart_item"), 
    path('delete_cart_item/<int:id>', views.delete_cart_item, name="delete_cart_item"), 
    path('checkout', views.checkout, name='checkout'),
    path("add_checkout_address", views.add_checkout_address, name="add_checkout_address"),
    path('delete_checkout_address/<int:id>', views.delete_checkout_address, name='delete_checkout_address'),
    path('edit_checkout_address/<int:id>', views.edit_checkout_address, name='edit_checkout_address'),
    path('order_summary/<int:address_id>/<int:order_id>', views.order_summary, name='order_summary'),
    path('my_orders', views.my_orders, name='my_orders'),
    path('cancel_order/<int:order_id>/<int:product_id>', views.cancel_order, name='cancel_order'),
    path('invoice/<int:address_id>/<int:order_id>', views.invoice, name="invoice"),
    path('payment/<int:address_id>', views.payment, name='payment'),
    path('razorpay/<int:address_id>/<str:after_tax_amount>', views.razor, name="razorpay"),
    path('single_order/<int:order_id>/<int:product_id>', views.single_order, name="single_order")
]

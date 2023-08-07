from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('adm_login', views.adm_login, name='adm_login'),
    path('adm_logout', views.adm_logout, name='adm_logout'),
    path('user_details', views.user_details, name='user_details'),
    path('block_user/<int:id>', views.Admin_block_user, name='block_user'),
    path('unblock_user/<int:id>', views.Admin_unblock_user, name='unblock_user'),
    path('adm_categories', views.adm_categories, name='adm_categories'),
    path('add_adm_categories', views.add_adm_categories, name='add_adm_categories'),
    path('edit_adm_categories/<int:id>', views.edit_adm_categories, name='edit_adm_categories'),
    path('delete_adm_categories/<int:id>', views.delete_adm_categories, name='delete_adm_categories'),
    path('adm_product', views.adm_product, name='adm_product'),
    path('add_adm_product', views.add_adm_product, name='add_adm_product'),
    path('edit_adm_product/<int:id>', views.edit_adm_product, name='edit_adm_product'),
    path('delete_adm_product/<int:id>', views.delete_adm_product, name='delete_adm_product'),
    path('adm_order', views.adm_order, name='adm_order'),
    path('product_color', views.product_color, name='product_color'),
    path('add_product_color', views.add_product_color, name='add_product_color'),
    path('edit_product_color/<int:id>', views.edit_product_color, name='edit_product_color'),
    path('delete_product_color/<int:id>', views.delete_product_color, name='delete_product_color'),
    path('product_size', views.product_size, name='product_size'),
    path('add_product_size', views.add_product_size, name='add_product_size'),
    path('edit_product_size/<int:id>', views.edit_product_size, name='edit_product_size'),
    path('delete_product_size/<int:id>', views.delete_product_size, name='delete_product_size'),
]

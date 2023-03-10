from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('sign_up/', sign_up, name='sign_up'),
    path('my_profile/', my_profile, name='my_profile'),
    path('seller_header/',seller_header, name='seller_header'),
    path('seller_register/',seller_register, name='seller_register'),
    path('seller_otp', seller_otp, name='seller_otp'),
    path('seller_login/', seller_login, name='seller_login'),
    path('seller_logout/', seller_logout, name='seller_logout'),
    path('my_orders/',my_orders, name="my_orders"),
    path('add_products/', add_products, name='add_products'),
    path('my_products/', my_products, name='my_products'),
    path('edit_product/<int:pk>', edit_product, name='edit_product'),
    path('del_product/<int:pk>', del_product, name='del_product')
]

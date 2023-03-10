from django.urls import path
from .views import *

urlpatterns = [
    path('',index, name='index'),
    path('main/',main, name='main'),
    path('faqs/',faqs, name='faqs'),
    path('about/',about, name='about'),
    path('contact/',contact, name='contact'),
    path('help/',help, name='help'),
    path('icons/',icons, name='icons'),
    path('checkout/', checkout, name='checkout'),
    path('payment/', payment, name='payment'),
    path('privacy/', privacy, name='privacy'),
    path('product/', product, name='product'),
    path('product2/', product2, name='product2'),
    path('single/', single, name='single'),
    path('single2/', single2, name='single2'),
    path('terms/', terms, name='terms'),
    path('typography/', typography, name='typography'),

    path('create_row', create_row, name='create_row'),

    path('register/', register, name='register'),
    path('otp/', otp, name='otp'),
    path('login/',login, name='login'),
    path('logout/', logout, name = 'logout'),
    path('forgot_password/',forgot_password, name='forgot_password'),    
    path('buyer_edit_profile/', buyer_edit_profile, name='buyer_edit_profile'),
    path('change_password/', change_password, name='change_password'),
    path('add_to_cart/<int:pk>', add_to_cart, name='add_to_cart'),
    path('my_cart/', my_cart, name='my_cart'),
    path('remove_product/<int:pk>', remove_product, name='remove_product'),
    path('my_cart/paymenthandler/', paymenthandler, name='paymenthandler'),
]

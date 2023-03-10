from ast import Delete
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def dashboard(request):
    try:
        seller_data = Seller.objects.get(email = request.session['seller_email'])
        return render(request, 'dashboard.html', {'seller_data':seller_data})
    except:
        return render(request,'auth-login.html')
    
def sign_up(request):
    return render(request,'sign-up.html')

def my_profile(request):
    return render(request, 'my-profile.html')

def seller_header(request):
    return render(request, 'seller_header.html')

def seller_register(request):
    if request.method == 'POST':
        try:
            Seller.objects.get(email = request.POST['email'])
            return render(request, 'auth-register.html',{'msg': 'Email already registered'})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                global seller_dict
                seller_dict = {
                    'username': request.POST['username'],
                    'email': request.POST['email'],
                    'password': request.POST['password']
                } 
                global cg_otp
                cg_otp = random.randint(1000,9999)
                subject = 'Seller Registration'
                message = f"hello {seller_dict['username']},\nYour otp is {cg_otp}"
                from_mail = settings.EMAIL_HOST_USER
                r_mail =  [seller_dict['email']]
                send_mail(subject,message,from_mail,r_mail)
                return render(request, '02seller_otp.html',{'msg': 'check your mail box !!'})
            else:
                return render(request, 'auth-register.html',{'msg': 'Password Does not match!!'})
    else:
        return render(request, 'auth-register.html')

def seller_otp(request):
    if cg_otp == int(request.POST['otp']):
        Seller.objects.create(
            full_name = seller_dict['username'],
            email = seller_dict['email'],
            password = seller_dict['password']
        )
        return render(request, 'auth-login.html', {'msg':'Hurray!! your account has been created successfully!!'})
    else:
        return render(request, '02seller_otp.html', {'msg':'Your otp is wrong. Please enter again!!'})

def seller_login(request):
    if request.method == 'POST':
        try:
            seller_data = Seller.objects.get(email = request.POST['email'])
            if request.POST['password'] == seller_data.password:
                request.session['seller_email'] = seller_data.email
                return redirect('dashboard')
            else:
                return render(request, 'auth-login.html',{'msg':'password is incorrect'})
        except:
            return render(request, 'auth-login.html', {'msg':f'This email "{request.POST["email"]}" is not registered.'})
    else:
        try:
            request.session['seller_email']
            return redirect('dashboard')
        except:
            return render(request, 'auth-login.html') 

def seller_logout(request):
    del request.session['seller_email']
    return redirect('dashboard')

def add_products(request):
    seller_data = Seller.objects.get(email = request.session['seller_email'])
    if request.method == 'POST':
        try:
            Product.objects.create(
                product_name = request.POST['product_name'],
                des = request.POST['description'],
                price = request.POST['price'],
                pic = request.FILES['pic'],
                seller = seller_data
            )
            return render(request, '04add_products.html', {'msg':'Product added successfully'})
        except:
            Product.objects.create(
                product_name = request.POST['product_name'],
                des = request.POST['description'],
                price = request.POST['price'],
                seller = seller_data
            )
            return render(request, '04add_products.html', {'msg':'Product added successfully'})
    else:
        return render(request, '04add_products.html' , {'seller_data': seller_data})

def my_products(request):
    seller_data = Seller.objects.get(email = request.session['seller_email'])
    session_seller_product = Product.objects.filter(seller = seller_data)
    return render(request, '05my_products.html',{ 'seller_data' : seller_data , 'user_products': session_seller_product})    

def my_orders(request):
    return redirect('dashboard')

def edit_product(request,pk):
    seller_data = Seller.objects.get(email = request.session['seller_email'])
    product_object = Product.objects.get(id = pk)
    if request.method == 'POST':
        product_object.product_name = request.POST['product_name']
        product_object.des = request.POST['description']
        product_object.price = request.POST['price']
        try:
            product_object.pic = request.FILES['pic']
            product_object.save()
            return render(request, '06edit_products.html', {'msg':'Product Updated Successfully!!', 'seller_data':seller_data, 'product_data':product_object})
        except:
            product_object.save()
            return render(request, '06edit_products.html', {'msg':'Product Updated Successfully!!', 'seller_data':seller_data, 'product_data':product_object})
    else:
        return render(request, '06edit_products.html', {'seller_data':seller_data, 'product_data':product_object})     

def del_product(request, pk):
    seller_data = Seller.objects.get(email = request.session['seller_email'])
    session_seller_product = Product.objects.filter(seller = seller_data)
    try:
        product_object = Product.objects.get(id = pk)
        product_object.delete()
        return render(request, '05my_products.html', {'seller_data':seller_data,'user_products':session_seller_product})
    except:
        return render(request, '05my_products.html', {'seller_data':seller_data,'user_products':session_seller_product})


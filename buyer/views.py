import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from buyer.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from seller.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# Create your views here.


def index(request):
    all_products = Product.objects.all()
    try:
        user_row = BuyerDemo.objects.get(email=request.session['email'])
        return render(request, 'index.html', {'user_data': user_row, 'all_products': all_products})
    except:
        return render(request, 'index.html', {'all_products': all_products})


def main(request):
    return render(request, 'main.html')


def faqs(request):
    return render(request, 'faqs.html')


def contact(request):
    return render(request, 'contact.html')


def icons(request):
    return render(request, 'icons.html')


def about(request):
    return render(request, 'about.html')


def checkout(request):
    return render(request, 'checkout.html')


def payment(request):
    return render(request, 'payment.html')


def privacy(request):
    return render(request, 'privacy.html')


def product(request):
    return render(request, 'product.html')


def product2(request):
    return render(request, 'product2.html')


def single(request):
    return render(request, 'single.html')


def single2(request):
    return render(request, 'single2.html')


def terms(request):
    return render(request, 'terms.html')


def typography(request):
    return render(request, 'typography.html')


def create_row(request):
    BuyerDemo.objects.create(
        first_name='yug',
        last_name='tandel',
        email='yugtandel05@gmail.com',
        password=123
    )
    return HttpResponse('row created successfully')
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------


# registeration process
def register(request):
    if request.method == 'POST':

        try:
            BuyerDemo.objects.get(email=request.POST['email'])
            return render(request, 'register.html', {'msg': 'Email is already registered'})

        except ObjectDoesNotExist:
            if request.POST['password'] == request.POST['repassword']:
                global user_dict
                user_dict = {
                    'first_name': request.POST['first_name'],
                    'last_name': request.POST['last_name'],
                    'mobile': request.POST['phone'],
                    'email': request.POST['email'],
                    'password': request.POST['password'],
                }
                global c_otp
                c_otp = random.randint(1000, 9999)
                subject = 'Email Verification'
                message = f'Hello {request.POST["first_name"]},\nYour OTP is {c_otp}'
                from_mail = settings.EMAIL_HOST_USER
                r_list = [(request.POST['email'])]
                send_mail(subject, message, from_mail, r_list)
                return render(request, 'otp.html')
            else:
                return render(request, 'register.html', {'say': 'Both password does not match'})
    else:
        return render(request, 'register.html')


def otp(request):
    if str(c_otp) == str(request.POST['u_otp']):
        BuyerDemo.objects.create(
            first_name=user_dict['first_name'],
            last_name=user_dict['last_name'],
            mobile=user_dict['mobile'],
            email=user_dict['email'],
            password=user_dict['password']
        )
        return HttpResponse('HURRAY !!! Your account has been')
    else:
        return render(request, 'otp.html', {'msg': 'otp does not match'})


def login(request):
    if request.method == 'POST':
        try:
            user_row = BuyerDemo.objects.get(email=request.POST['email'])
            if request.POST['password'] == user_row.password:
                request.session['email'] = user_row.email
                print(user_row)
                return redirect('index')
            else:
                return render(request, 'login.html', {'msg': 'password is incorrect'})
        except:
            return render(request, 'login.html', {'msg': 'Email not registered'})
    else:
        try:
            request.session['email']
            return redirect('index')
        except:
            return render(request, 'login.html')


def forgot_password(request):
    if request.method == 'POST':
        try:
            user_row = BuyerDemo.objects.get(email=request.POST['email'])

            subject = 'Get Your Password!!!'
            message = f'hello, {user_row.first_name},\nYour password is {user_row.password}.'
            from_email = settings.EMAIL_HOST_USER
            list1 = [request.POST['email']]
            send_mail(subject, message, from_email, list1)
            return render(request, 'login.html', {'say': 'We have sent your password to your MailBox'})
        except:
            return render(request, 'forgot_pass.html', {'say': 'Email not registered'})

    else:
        return render(request, 'forgot_pass.html')


def logout(request):
    del request.session['email']
    return redirect('index')


def buyer_edit_profile(request):
    if request.method == 'POST':
        user_data = BuyerDemo.objects.get(email=request.session['email'])
        user_data.first_name = request.POST['first_name']
        user_data.last_name = request.POST['last_name']
        user_data.mobile = request.POST['mobile']
        user_data.address = request.POST['address']
        try:
            user_data.pic = request.FILES['pic']
            user_data.save()
            return render(request, 'buyer_edit_profile.html', {'user_data': user_data})
        except:
            user_data.save()
            return render(request, 'buyer_edit_profile.html', {'user_data': user_data})
    else:
        try:
            user_data = BuyerDemo.objects.get(email=request.session['email'])
            return render(request, 'buyer_edit_profile.html', {'user_data': user_data})
        except:
            return render(request, 'login.html', {'user_data': user_data})
        return render(request, 'buyer_edit_profile.html')


def change_password(request):
    if request.method == 'POST':
        try:
            user_data = BuyerDemo.objects.get(email=request.session['email'])
            if request.POST['old_password'] == user_data.password:
                if request.POST['new_password'] == request.POST['re_password']:
                    user_data.password = request.POST['new_password']
                    user_data.save()
                    return render(request, 'change_password.html', {'msg': 'Password changed successfully'})
                else:
                    return render(request, 'change_password.html', {'msg': 'Both password does no match'})
            else:
                return render(request, 'change_password.html', {'msg': 'your current password is incorrect'})
        except:
            return render(request, 'login.html')
    else:
        return render(request, 'change_password.html')


def add_to_cart(request, pk):
    try:
        buyer_obj = BuyerDemo.objects.get(email=request.session['email'])
        product_obj = Product.objects.get(id=pk)
        Cart.objects.create(
            product=product_obj,
            buyer=buyer_obj
        )
        return redirect('index')
    except:
        return render(request, 'login.html')


def my_cart(request):
    if request.method == 'GET':
        try:
        # if(1):
            buyer_obj = BuyerDemo.objects.get(email=request.session['email'])
            cart_list = Cart.objects.filter(buyer=buyer_obj)
            # print(cart_list[0].buyer.first_name)
            # print((cart_list[0]))
            # print((cart_list[1]))
            # print((cart_list[2]))
            # print((cart_list[3]))
            total_products = len(cart_list)
            global total_price
            total_price = 0
            for i in list(cart_list):
                # print(i.product.seller)
                # print(i.product.price) 
                total_price = total_price + i.product.price

            # payment nu button jivit karva maate no code
            currency = 'INR'
            amount = float(total_price*8000)  # total_price is in dollar 

            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                            currency=currency,
                                                            payment_capture='0'))

            # order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            callback_url = 'paymenthandler/'

            # we need to pass these details to frontend.
            context = {}
            context['razorpay_order_id'] = razorpay_order_id
            context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            context['razorpay_amount'] = amount
            context['currency'] = currency
            context['callback_url'] = callback_url
            context.update({'cart_list': cart_list, 'total_price': total_price, 'total_products': total_products})
            print(total_price)
            return render(request, 'my_cart.html', context=context )
        except:
        # else:
            return HttpResponse('error')
    else:
        return HttpResponse('this is post method part')


def remove_product(request, pk):
    c_delete = Cart.objects.get(id=pk)
    c_delete.delete()
    return redirect('my_cart')


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))





# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = float(total_price*8000)  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # buyer_obj = BuyerDemo.objects.get(email=request.session['email'])
                    # cart_list = Cart.objects.filter(buyer=buyer_obj)
                    # cart_list[0].product.delete()
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()

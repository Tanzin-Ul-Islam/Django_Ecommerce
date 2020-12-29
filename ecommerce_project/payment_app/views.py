from django.shortcuts import render,HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from payment_app.models import BillingAddress
from order_app.models import Order, Cart
from payment_app.forms import BillingForm
from django.contrib import messages
#secret keys
from payment_app.secret_settings import store_id, secret_key
#for payment
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
#to avoid csrf token
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)[0]
    form = BillingForm(instance=saved_address)
    if request.method == "POST":
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.info(request, "Shipping Address saved!")
    order_qs = Order.objects.filter(user=request.user, ordered=False)[0]
    order_items = order_qs.orderitems.all()
    order_total = order_qs.get_totals()
    return render(request, 'payment_app/checkout.html', context={'form':form, 'order_total':order_total, 'order_items':order_items,
                                                                 'saved_address':saved_address})

@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    if not saved_address[0].is_fully_filled():
        messages.info(request, "Please fill up the shipping address!")
        return redirect("payment_app:checkout")
    if not request.user.profile.is_fully_filled():
        messages.info(request, "Please complete profile details!")
        return redirect("login_app:profile")
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id,
                            sslc_store_pass=secret_key)

    url_status = request.build_absolute_uri(reverse("payment_app:payment_status"))
    mypayment.set_urls(success_url=url_status, fail_url=url_status,
                       cancel_url=url_status, ipn_url=url_status)

    order_qs=Order.objects.filter(user=request.user)[0]
    order_items=order_qs.orderitems.all()
    order_items_count = order_qs.orderitems.count()
    order_total = order_qs.get_totals()
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed',
                                      product_name=order_items, num_of_item=order_items_count, shipping_method='Courier',
                                      product_profile='None')

    user_info = request.user
    print(user_info.email, user_info.profile.full_name)
    mypayment.set_customer_info(name=user_info.profile.full_name, email= user_info.email, address1=user_info.profile.address,
                                address2=user_info.profile.address, city=user_info.profile.city, postcode=user_info.profile.zipcode, country=user_info.profile.country,
                                phone=user_info.profile.phone)
    billing_address=saved_address[0]
    mypayment.set_shipping_info(shipping_to=user_info.profile.full_name, address=billing_address.address, city=billing_address.city, postcode=billing_address.zipcode,
                                country=billing_address.country)
    response_data = mypayment.init_payment()
    # print(url_status)
    # print(store_id)
    # print(secret_key)
    #print(response_data)
    return redirect(response_data['GatewayPageURL'])

@csrf_exempt
def payment_status(request):
    if request.method == 'POST' or request.method == 'post':
        payment_info = request.POST
        status = payment_info['status']
        print(payment_info)
        if status == 'VALID':
            tran_id = payment_info['tran_id']
            val_id = payment_info['val_id']
            messages.success(request, "Your payment completed successfully!")
            return HttpResponseRedirect(reverse('payment_app:purchased', kwargs={'tran_id':tran_id, 'val_id':val_id},))

        elif status == 'FAILED':
            messages.error(request, "Your payment failed!!! Please try again.")
    return render(request, 'payment_app/payment_status.html')

@login_required
def purchased(request, tran_id, val_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)[0]
    order_qs.ordered = True
    order_qs.payment = val_id
    order_qs.orderId = tran_id
    order_qs.save()
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse("shop_app:home"))
@login_required
def my_orders(request):
    diction = {}
    try:
        orders = Order.objects.filter(user = request.user, ordered = True)
        diction.update({'orders':orders})
    except:
        messages.warning(request, "You Don't Have Any Complete Oreder!")
        return redirect('shop_app:home')
    return render(request, 'payment_app/my_order.html', context=diction)

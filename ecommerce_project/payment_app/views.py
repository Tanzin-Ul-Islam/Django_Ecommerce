from django.shortcuts import render,HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from payment_app.models import BillingAddress
from order_app.models import Order
from payment_app.forms import BillingForm
from django.contrib import messages

#for payment
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal

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
    store_id = 'abc5fe992b13f888'
    secret_key = 'abc5fe992b13f888@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id,
                            sslc_store_pass=secret_key)

    url_status = request.build_absolute_uri(reverse("payment_app:payment_status"))
    print(url_status)



    return render(request, 'payment_app/payment.html')


@login_required
def payment_status(request):
    return render(request, 'payment_app/payment_status.html')
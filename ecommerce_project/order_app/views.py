from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from order_app.models import Cart, Order
from shop_app.models import Product
from django.contrib import messages

# Create your views here.
@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item = item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "This item quantity was updated.")
            return redirect('order_app:cart')
        else:
            order.orderitems.add(order_item[0])
            messages.info(request,"Item has been added to cart")
            return redirect('order_app:cart')
    else:
        order = Order(user = request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, "Item was added to Cart")
        return redirect('shop_app:home')

@login_required
def cart_view(request):
    carts = Cart.objects.filter(user = request.user, purchased=False)
    order = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and order.exists():
        order = order[0]
        return render(request, 'order_app/cart.html', context={'carts':carts, 'order':order})
    else:
        return render(request, 'order_app/cart.html', context={'message':"Cart is empty!"})
@login_required
def remove_cart_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item = item, user= request.user, purchased = False)
            order_item = order_item[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            if order.orderitems.count() == 0:
                messages.info(request, "You don't have an active order!")
                return redirect("shop_app:home")
            else:
                messages.warning(request, "Item was removed from your cart!")
                return redirect("order_app:cart")
        else:
            messages.info(request, "This item is not in your cart.")
            return redirect("shop_app:home")
    else:
        messages.info(request, "You don't have any order!")
        return redirect("shop_app:home")
@login_required
def increase_item_quantity(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                return redirect("order_app:cart")
            else:
                messages.info(request, "This item is not included to the cart!")
                return redirect("order_app:cart")

        else:
            messages.info(request, "This item is not in your cart.")
            return redirect("shop_app:home")

    else:
        messages.info(request, "You don't have an active order!")
        return redirect("shop_app:home")

@login_required
def decrease_item_quantity(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                return redirect("order_app:cart")
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.info(request, "Item has been removed from the cart!")
                return redirect("order_app:cart")

        else:
            messages.info(request, "This item is not in your cart.")
            return redirect("shop_app:home")

    else:
        messages.info(request, "You don't have an active order!")
        return redirect("shop_app:home")
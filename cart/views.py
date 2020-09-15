from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Order, CartItem
from medicines.models import Medicine
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def cartview(request):
    orders = Order.objects.filter(user=request.user, ordered=False)
    items = CartItem.objects.filter(user=request.user)
    if orders.exists():
        order = orders[0]
        return render(request, "cart/view.html", {"items": items})

    return redirect(reverse_lazy("medicines:all"))


def add_to_cart(request, slug):
    a = request.META.get("HTTP_REFERER")
    # if not a:
    #     messages.error(request, "You cannot edit cart items this way")
    #     return redirect(reverse_lazy("medicines:all"))
    item = get_object_or_404(Medicine, slug=slug)
    order_item = CartItem.objects.create(user=request.user, item=item)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity updated.")
        else:
            order.items.add(order_item)
            messages.success(request, "Item added to the cart")
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
        messages.success(request, "Item added to the cart")
    return redirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, slug):
    a = request.META.get("HTTP_REFERER")
    if not a:
        messages.error(request, "You cannot edit cart items this way")
        return redirect(reverse_lazy("medicines:all"))
    item = get_object_or_404(Medicine, slug=slug)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = CartItem.objects.filter(user=request.user, item=item)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.success(request, "Item deleted from the cart")
        else:
            messages.error(request, "Item was not in your cart")
    else:
        messages.error(request, "your cart is empty")
    return redirect(request.META.get("HTTP_REFERER"))


def increase_cart(request, slug):
    a = request.META.get("HTTP_REFERER")
    # if not a:
    #     messages.error(request, "You cannot edit cart items this way")
    #     return redirect(reverse_lazy("medicines:all"))
    item = get_object_or_404(Medicine, slug=slug)
    order_item = CartItem.objects.get(user=request.user, item=item)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity updated.")
        else:
            order.items.add(order_item)
            messages.success(request, "Item added to the cart")
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
        messages.success(request, "Item added to the cart")
    return redirect(request.META.get('HTTP_REFERER'))


def decrease_cart(request, slug):
    a = request.META.get("HTTP_REFERER")
    if not a:
        messages.error(request, "You cannot edit cart items this way")
        return redirect(reverse_lazy("medicines:all"))
    item = get_object_or_404(Medicine, slug=slug)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = CartItem.objects.filter(user=request.user, item=item)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "Item quantity updated")
            else:
                order.items.remove(order_item)
                order_item.delete()
                messages.success(request, "Item deleted from the cart")
        else:
            messages.error(request, "Item was not in your cart")
    else:
        messages.error(request, "your cart is empty")
    return redirect(request.META.get("HTTP_REFERER"))


def order_view(request):
    orders = Order.objects.filter(user=request.user, ordered=True)
    ctx = {"orders": orders}
    return render(request, "order/view.html", ctx)


def increase_cart_test(request, slug):
    a = request.META.get("HTTP_REFERER")
    # if not a:
    #     messages.error(request, "You cannot edit cart items this way")
    #     return redirect(reverse_lazy("medicines:all"))
    q = 0
    item = get_object_or_404(Medicine, slug=slug)
    order_item = CartItem.objects.get(user=request.user, item=item)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity updated.")
            q = order_item.quantity
        else:
            messages.error(request, "Item was not in the cart")
    else:
        messages.error(request, "Your cart is empty")
    return JsonResponse({'quantity': q})


def decrease_cart_test(request, slug):
    a = request.META.get("HTTP_REFERER")
    if not a:
        messages.error(request, "You cannot edit cart items this way")
        return redirect(reverse_lazy("medicines:all"))
    item = get_object_or_404(Medicine, slug=slug)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = CartItem.objects.filter(user=request.user, item=item)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "Item quantity updated")
                return JsonResponse({"quantity": order_item.quantity})
            else:
                order.items.remove(order_item)
                order_item.delete()
                messages.success(request, "Item deleted from the cart")
        else:
            messages.error(request, "Item was not in your cart")
    else:
        messages.error(request, "your cart is empty")
    return JsonResponse({"quantity": 0})

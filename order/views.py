from django.shortcuts import render, get_object_or_404
from .models import Order
from django.http import Http404

def thanks(request, order_id=None):
    customer_order = None
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)
        # stop people from changing the number in url to see other ppls details, only shows if order email is logged in account's email
        if customer_order.emailAddress != request.user.email:
            raise Http404("You are not authorized to view this order.")
    return render(request, 'thanks.html', {'customer_order': customer_order})
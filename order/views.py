from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404
from .models import Order

def thanks(request, order_id=None):
    customer_order = None
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)
    return render(request, 'thanks.html', {'customer_order': customer_order})
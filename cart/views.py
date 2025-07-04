from django.shortcuts import redirect, render, get_object_or_404
from sobaka.models import Human
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.urls import reverse
from order.models import Order, OrderItem
from stripe import StripeError
from uuid import UUID
from vouchers.models import Voucher
from vouchers.forms import VoucherCartApplyForm
from decimal import Decimal
from django.core.mail import send_mail
from datetime import date, timedelta
from .forms import BookingDateForm
from sobaka.models import UnavailableDate
from django.http import JsonResponse
import logging

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, human_id):
    product = Human.objects.get(id=human_id)
    booking_date = request.GET.get('booking_date')

    if booking_date:
        booking_date = date.fromisoformat(booking_date)
        if not product.is_available_on(booking_date):
            return redirect('cart:cart_detail')

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist: 
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.duration += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # defaults cart if nothing exists
        cart_item = CartItem.objects.create(product=product, duration=1, cart=cart)
    return redirect('cart:cart_detail')

def select_date(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id') 
        booking_date = request.POST.get('booking_date')

        if cart_item_id and booking_date:
            booking_date = date.fromisoformat(booking_date)  # makes string into date
            cart_item = get_object_or_404(CartItem, id=cart_item_id)
            # checking date for product human
            if not cart_item.product.is_available_on(booking_date):
                # error msg if they try book, should not show up but just in case
                return render(request, 'cart.html', {
                    'cart_items': CartItem.objects.filter(cart=cart_item.cart, active=True),
                    'error': f"{cart_item.product.name} is not available on {booking_date}. Please select another date.",
                })

            # save date to cart/order
            cart_item.selected_date = booking_date
            cart_item.save()

        return redirect('cart:cart_detail')
    return redirect('cart:cart_detail')

def get_unavailable_dates(request, human_id):
    human = get_object_or_404(Human, id=human_id)
    unavailable_dates = human.unavailable_dates.values_list('date', flat=True)
    return JsonResponse(list(unavailable_dates), safe=False)

def cart_detail(request, total=0, counter=0, cart_items=None):
    discount = 0
    voucher_id = 0
    new_total = 0
    voucher = None
    error = None

    try:
        # Retrieve the cart using the session ID
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # Get all active cart items for the cart
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        
        # Calculate the total price and item count
        for cart_item in cart_items:
            # Include duration in the total price calculation
            total += (cart_item.product.price * cart_item.duration)
            counter += cart_item.duration
        
        # Check if a voucher is applied and calculate the discount
        voucher_id = request.session.get('voucher_id')
        if voucher_id and total > 0:
            voucher = Voucher.objects.get(id=voucher_id)
            discount = (total * (voucher.discount / Decimal('100')))
            new_total = (total - discount)
        else:
            new_total = total

        # Fetch unavailable dates for each human in the cart
        unavailable_dates = {
            str(cart_item.product.id): list(cart_item.product.unavailable_dates.values_list('date', flat=True))
            for cart_item in cart_items
        }

    except ObjectDoesNotExist:
        request.session['voucher_id'] = None
        unavailable_dates = {}

    # Set up Stripe payment details
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)  # Convert total to cents
    description = 'Sobaka - New Booking'
    voucher_apply_form = VoucherCartApplyForm()

    if request.method == 'POST':
        try:
            # Create a Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Booking from Sobaka Model Agency',
                        },
                        'unit_amount': stripe_total,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                billing_address_collection='required',
                shipping_address_collection={},
                payment_intent_data={'description': description},
                success_url=request.build_absolute_uri(reverse('cart:new_order')) + f"?session_id={{CHECKOUT_SESSION_ID}}&voucher_id={voucher_id}&cart_total={total}",
                cancel_url=request.build_absolute_uri(reverse('cart:cart_detail')),
            )
            # Redirect to the Stripe checkout page
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            # Render the template with an error message
            return render(request, 'cart.html', {
                'cart_items': cart_items,
                'total': total,
                'counter': counter,
                'error': str(e),  # Display error if there's an issue with Stripe
            })

    booking_date_form = BookingDateForm()

    # Render the cart template with the cart details
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
        'voucher': voucher,
        'discount': discount,
        'new_total': new_total,
        'voucher_apply_form': voucher_apply_form,
        'unavailable_dates': unavailable_dates,
        'stripe_total': stripe_total,
        'description': description,
        'error': error,
    })

def cart_remove(request, human_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Human, id=human_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.duration > 1:
        cart_item.duration -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def full_remove(request, human_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Human, id=human_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.selected_date = None  # set the date back to none/default
    cart_item.delete()
    if not CartItem.objects.filter(cart=cart).exists():
        request.session['voucher_id'] = None

    return redirect('cart:cart_detail')

def empty_cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            cart_item.selected_date = None  # same as full remove for date but loops for all humans/dates
            cart_item.save()
        cart_items.delete()
        cart.delete()
        request.session['voucher_id'] = None
        return redirect('sobaka:all_humans')
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cart_detail')

def create_order(request):
    logger = logging.getLogger('custom_logger') 
    try: 
        session_id = request.GET.get('session_id') 
        if not session_id:
            logger.error("Session ID not found.") 
            raise ValueError("Session ID not found.") 

        try: 
            session = stripe.checkout.Session.retrieve(session_id) 
            logger.info(f"Stripe session retrieved: {session}")
        except StripeError as e: 
            logger.error(f"Stripe Error: {e}")
            return redirect("sobaka:all_humans")  

        customer_details = session.customer_details 
        if not customer_details or not customer_details.address: 
            logger.error("Missing information in the Stripe session.")
            raise ValueError("Missing information in the Stripe session.") 

        billing_address = customer_details.address 
        billing_name = customer_details.name 
        shipping_address = customer_details.address 
        shipping_name = customer_details.name 

        try: 
            order_details = Order.objects.create( 
                token=session.id, 
                total=session.amount_total / 100,  # Convert cents to currency units 
                emailAddress=customer_details.email, 
                billingName=billing_name, 
                billingAddress1=billing_address.line1, 
                billingCity=billing_address.city, 
                billingPostcode=billing_address.postal_code, 
                billingCountry=billing_address.country, 
                shippingName=shipping_name, 
                shippingAddress1=shipping_address.line1,  
                shippingCity=shipping_address.city,  
                shippingPostcode=shipping_address.postal_code, 
                shippingCountry=shipping_address.country, 
            ) 
            order_details.save() 
            logger.info(f"Order created: {order_details}")
        except Exception as e:  
            logger.error(f"Error creating order: {e}") 
            return redirect("sobaka:all_humans")  

        try: 
            cart = Cart.objects.get(cart_id=_cart_id(request)) 
            cart_items = CartItem.objects.filter(cart=cart, active=True) 
            logger.info(f"Cart retrieved: {cart}, Items: {[str(item) for item in cart_items]}")
        except ObjectDoesNotExist: 
            logger.error("Cart or cart items not found.")
            return redirect("sobaka:all_humans") 
        except Exception as e: 
            logger.error(f"Error retrieving cart: {e}") 
            return redirect("sobaka:all_humans") 

        # Retrieve voucher from session
        voucher_id = request.session.get('voucher_id')
        voucher = Voucher.objects.get(id=voucher_id) if voucher_id else None

        if voucher:
            cart_total = sum(item.product.price * item.duration for item in cart_items)
            order_details.voucher = voucher
            order_details.discount = cart_total * (voucher.discount / Decimal('100'))
            order_details.total = cart_total - order_details.discount
            order_details.save()

        for item in cart_items: 
            try: 
                oi = OrderItem.objects.create( 
                    product=item.product.name, 
                    duration=item.duration, 
                    price=item.product.price,
                    booked_date=item.selected_date, 
                    order=order_details 
                ) 
                logger.info(f"Order item created: {oi}")
                if voucher:
                    discount = oi.price * (voucher.discount / Decimal('100'))
                    oi.price -= discount
                oi.save()

                # point in create order view where the selected date is added to the unavailable dates model
                if item.selected_date:
                    UnavailableDate.objects.create(human=item.product, date=item.selected_date)
                    logger.info(f"Unavailable date added: {item.selected_date} for {item.product}")

            except Exception as e: 
                logger.error(f"Error processing item {item.id}: {e}")
                continue 

        # Send confirmation email
        try:
            send_email(request, order_details)
            logger.info(f"Confirmation email sent for order: {order_details.id}")
        except Exception as e:
            logger.error(f"Error sending email: {e}")

        # Empty the cart
        empty_cart(request) 
        logger.info("Cart emptied successfully.")

        # Redirect to the "Thank You" page with the order ID
        return redirect('order:thanks', order_id=order_details.id)
    
    except ValueError as ve: 
        logger.error(f"ValueError: {ve}") 
        return redirect("sobaka:all_humans") 

    except StripeError as se: 
        logger.error(f"Stripe Error: {se}") 
        return redirect("sobaka:all_humans")  

    except Exception as e: 
        logger.critical(f"Unexpected error: {e}") 
        return redirect("sobaka:all_humans")

def send_email(request, order_id):
    try:
        send_mail(
            'Your order',
            'Thank you for your order!',
            'no-reply@sobaka.com',
            ['p@c.ie'],
            fail_silently=False,
            html_message=f"<p>Dear {request.user.username},</p><p>Thank you for your order. Your order number is {order_id.id}</p>"
        )
    except Exception as e:
        print(f"Email failed: {e}")
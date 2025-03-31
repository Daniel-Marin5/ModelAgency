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

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def update_duration(request, human_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Human, id=human_id)  # Ensure this works with UUID
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        new_duration = int(request.POST.get('duration', cart_item.duration))  # Get new duration from POST data
        cart_item.duration = new_duration
        cart_item.save()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart:cart_detail')

def add_cart(request, human_id):
    product = Human.objects.get(id=human_id)
    duration = int(request.POST.get('duration', 1))  # Get duration from POST data (default to 1 hour)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist: 
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if (cart_item.quantity < cart_item.product.available):
            cart_item.quantity += 1
            cart_item.duration = duration  # Update duration
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, duration=duration, cart=cart)
    return redirect('cart:cart_detail')

def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        # Retrieve the cart using the session ID
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # Get all active cart items for the cart
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        
        # Calculate the total price and item count
        for cart_item in cart_items:
            # Include duration in the total price calculation
            total += (cart_item.product.price * cart_item.quantity * cart_item.duration)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    # Set up Stripe payment details
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)  # Convert total to cents
    description = 'Sobaka - New Booking'

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
                success_url=request.build_absolute_uri(reverse('cart:new_order')) + f"?session_id={{CHECKOUT_SESSION_ID}}",
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

    # Render the cart template with the cart details
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
    })

def cart_remove(request, human_id):
    cart= Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Human, id=human_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def full_remove(request, human_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Human, id=human_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')

def empty_cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        cart_items.delete()
        cart.delete()
        return redirect('sobaka:all_humans')
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cart_detail')

def create_order(request): 
    try: 
        session_id = request.GET.get('session_id') 
        if not session_id: 
            raise ValueError("Session ID not found.") 

        try: 
            session = stripe.checkout.Session.retrieve(session_id) 
        except StripeError as e: 
            return redirect("sobaka:all_humans")  

        customer_details = session.customer_details 
        if not customer_details or not customer_details.address: 
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
        except Exception as e:  
            print(f"Error: {e}") 
            return redirect("sobaka:all_humans")  

        try: 
            cart = Cart.objects.get(cart_id=_cart_id(request)) 
            cart_items = CartItem.objects.filter(cart=cart, active=True) 

        except ObjectDoesNotExist: 
            return redirect("sobaka:all_humans") 
        except Exception as e: 
            print(f"Error: {e}") 
            return redirect("sobaka:all_humans") 

        for item in cart_items: 
            try: 
                oi = OrderItem.objects.create( 
                    product=item.product.name, 
                    quantity=item.quantity, 
                    price=item.product.price, 
                    duration=item.duration,  # Include duration
                    order=order_details 
                ) 
                oi.save() 
            except Exception as e: 
                print(f"Error processing item {item.id}: {e}")
                continue  # Log error and continue processing other items

        empty_cart(request) 

        # Redirect to the "Thank You" page with the order ID
        return redirect('order:thanks', order_id=order_details.id)
    
    except ValueError as ve: 
        print(f"Error: {ve}") 
        return redirect("sobaka:all_humans") 

    except StripeError as se: 
        print(f"Stripe Error: {se}") 
        return redirect("sobaka:all_humans")  

    except Exception as e: 
        print(f"Unexpected error: {e}") 
        return redirect("sobaka:all_humans")
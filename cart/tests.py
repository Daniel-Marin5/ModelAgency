from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem

# Create your tests here.
class ShoppingCartTests(TestCase):

    def setUp(self):
        # Create a sample product
        self.product = Product.objects.create(name='Ruth', price=150.00)

        # Create a user for authenticated tests
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_add_cart_item(self):
        response = self.client.post(reverse('cart:add', kwargs={'product_id': self.product.id}), data={'quantity': 1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ruth')
        self.assertEqual(CartItem.objects.count(), 1)

    def test_update_cart_item(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        response = self.client.post(reverse('cart:update', kwargs={'product_id': self.product.id}), data={'quantity': 3})
        self.assertEqual(response.status_code, 200)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 3)

    def test_remove_cart_item(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        response = self.client.post(reverse('cart:remove', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_cart_total_price(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        response = self.client.get(reverse('cart:summary'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Total: £300.00')

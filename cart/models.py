from django.db import models
from sobaka.models import Human

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Human, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    duration = models.IntegerField(default=1)
    selected_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.price * self.duration
    
    def __str__(self):
        return f"{self.product.name} (Duration: {self.duration} hours)"
1

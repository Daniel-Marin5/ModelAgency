from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class VoucherCartApplyForm(forms.Form):
    code = forms.CharField(label="Voucher Code", max_length=50)

class VoucherApplyForm(forms.Form): # different model for adding/editing in admin profile since it broke the cart view
    code = forms.CharField(label="Voucher Code", max_length=50)
    discount = forms.IntegerField(
        label="Discount (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
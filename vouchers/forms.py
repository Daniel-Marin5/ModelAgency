from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class VoucherApplyForm(forms.Form):
    code = forms.CharField(label="Voucher Code", max_length=50)
    discount = forms.IntegerField(
        label="Discount (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from .models import Voucher
from .forms import VoucherApplyForm, VoucherCartApplyForm

def voucher_apply(request):
    now = timezone.now()
    if request.method == 'POST':
        form = VoucherCartApplyForm(request.POST) #changed to new model
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                voucher = Voucher.objects.get(
                    code__iexact=code,
                    valid_from__lte=now,
                    valid_to__gte=now,
                    active=True
                )
                request.session['voucher_id'] = voucher.id
            except Voucher.DoesNotExist:
                request.session['voucher_id'] = None
        else:
            request.session['voucher_id'] = None

    return redirect('cart:cart_detail')

@login_required
def add_voucher(request):
    if not request.user.permissions:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = VoucherApplyForm(request.POST)
        if form.is_valid():
            Voucher.objects.create(
                code=form.cleaned_data['code'],
                valid_from=now(),
                valid_to=now() + timedelta(days=365),  # makes it default +1 year
                discount=form.cleaned_data['discount'], 
                active=True
            )
            return redirect('accounts:profile')
    else:
        form = VoucherApplyForm()
    return render(request, 'vouchers/add_voucher.html', {'form': form})

@login_required
def delete_voucher(request, voucher_id):
    if not request.user.permissions:
        return redirect('accounts:profile')

    voucher = get_object_or_404(Voucher, id=voucher_id)

    if request.method == 'POST':
        voucher.delete()
        return redirect('accounts:profile')
        
    return render(request, 'vouchers/delete_voucher.html', {'voucher': voucher})
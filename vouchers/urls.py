from django.urls import path
from . import views

app_name = 'vouchers'

urlpatterns = [
    path('apply/', views.voucher_apply, name='apply'),
    path('add/', views.add_voucher, name='add_voucher'),
    path('delete/<int:voucher_id>/', views.delete_voucher, name='delete_voucher'),
]
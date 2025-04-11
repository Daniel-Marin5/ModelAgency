from django.urls import path
from . import views

app_name='cart'

urlpatterns = [
    path('add/<uuid:human_id>/', views.add_cart, name='add_cart'),
    path('', views.cart_detail, name='cart_detail'),
    path('remove/<uuid:human_id>/', views.cart_remove, name='cart_remove'),
    path('full_remove/<uuid:human_id>/', views.full_remove, name='full_remove'),
    path('new_order/', views.create_order, name='new_order'),
    path('select_date/', views.select_date, name='select_date'),
    path('unavailable_dates/<uuid:human_id>/', views.get_unavailable_dates, name='get_unavailable_dates'),
]
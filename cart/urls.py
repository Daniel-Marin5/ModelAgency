from django.urls import path
from . import views

app_name='cart'

urlpatterns = [
    path('add/<uuid:human_id>/', views.add_cart, name='add_cart'),
    path('', views.cart_detail, name='cart_detail'),
    path('remove/<uuid:human_id>/', views.cart_remove, name='cart_remove'),
    path('full_remove/<uuid:human_id>/', views.full_remove, name='full_remove'),
    path('new_order/', views.create_order, name='new_order'),
    path('update_duration/<uuid:human_id>/', views.update_duration, name='update_duration'), 
]
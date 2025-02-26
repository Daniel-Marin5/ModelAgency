from django.urls import path
from . import views

app_name = 'sobaka'

urlpatterns = [
    path('', views.hum_list, name = 'all_humans'),
    path('<uuid:category_id>/', views.hum_list, name = 'humans_by_category'),
    path('<uuid:category_id>/<uuid:human_id>/', views.human_detail, name = 'human_detail'),
]
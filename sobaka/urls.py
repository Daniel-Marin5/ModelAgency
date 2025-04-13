from django.urls import path
from . import views

app_name = 'sobaka'

urlpatterns = [
    path('', views.hum_list, name = 'all_humans'),
    path('<uuid:category_id>/', views.hum_list, name = 'humans_by_category'),
    path('<uuid:category_id>/<uuid:human_id>/', views.human_detail, name = 'human_detail'),
    path('leave_review/<int:order_item_id>/', views.leave_review, name='leave_review'),
    path('add_human/', views.add_human, name='add_human'),
    path('edit_human/<uuid:human_id>/', views.edit_human, name='edit_human'),
    path('delete_human/<uuid:human_id>/', views.delete_human, name='delete_human'),
    path('news/', views.news_list, name='news'),
]
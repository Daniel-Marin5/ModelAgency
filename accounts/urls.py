from django.urls import path
from .views import SignUpView, ProfileView, toggle_permissions, delete_user

app_name = 'accounts'

urlpatterns = [
    path('create/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('toggle_permissions/<int:user_id>/', toggle_permissions, name='toggle_permissions'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
] 

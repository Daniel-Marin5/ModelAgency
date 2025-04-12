from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth import login, get_user_model
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from order.models import Order, OrderItem
from sobaka.models import Human
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from vouchers.models import Voucher
from django.core.paginator import Paginator

class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('sobaka:all_humans')

    def form_valid(self, form):
        response = super().form_valid(form)

        client_group, created = Group.objects.get_or_create(name='Client')
        self.object.groups.add(client_group)

        login(self.request, self.object)

        return response

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Fetch the user's orders
        user_orders = Order.objects.filter(emailAddress=user.email).order_by('-created')
        context['orders'] = user_orders
        # Fetch all models if the user has permissions
        if user.permissions:
            context['humans'] = Human.objects.all()
            User = get_user_model()
            context['accounts'] = User.objects.exclude(id=user.id)
            context['vouchers'] = Voucher.objects.all()  # Add vouchers to the context
        return context

@login_required
def toggle_permissions(request, user_id):
    if not request.user.permissions:
        return redirect('accounts:profile')  # Redirect if the user doesn't have permissions

    User = get_user_model()
    account = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        account.permissions = not account.permissions
        account.save()
    return redirect('accounts:profile')

@login_required
def delete_user(request, user_id):
    if not request.user.permissions:
        return redirect('accounts:profile')  # Redirect if the user doesn't have permissions

    User = get_user_model()
    account = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        account.delete()
        return redirect('accounts:profile')  # Redirect after deletion

    # Render the confirmation page for GET requests
    return render(request, 'accounts/delete_user.html', {'account': account})

@login_required
def view_bookings(request):
    if not request.user.permissions:
        return redirect('accounts:profile')  # Redirect if the user doesn't have permissions

    # Fetch all orders
    orders = Order.objects.all().order_by('-created')

    # Paginate the orders (20 rows per page)
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/view_bookings.html', {'page_obj': page_obj})
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from order.models import Order, OrderItem


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
        # Fetch the user's orders
        user_orders = Order.objects.filter(emailAddress=self.request.user.email).order_by('-created')
        context['orders'] = user_orders
        return context
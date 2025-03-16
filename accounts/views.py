from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import CustomUser


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

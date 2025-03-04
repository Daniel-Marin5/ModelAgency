from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import CustomUser


class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)

        client_group, created = Group.objects.get_or_create(name='Client')
        self.object.groups.add(client_group)

        login(self.request, self.object)

        return response

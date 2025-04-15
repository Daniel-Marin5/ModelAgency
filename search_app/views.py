from sobaka.models import Human
from django.views.generic import ListView
from django.db.models import Q

class SearchResultsListView(ListView):
    model = Human
    context_object_name = 'humans_list'
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        attribute = self.request.GET.get('attribute', 'name')
        if query:
            filter_kwargs = {f"{attribute}__icontains": query}
            return Human.objects.filter(**filter_kwargs)
        return Human.objects.all()

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        attribute = self.request.GET.get('attribute', 'name')
        attribute_labels = {
            'name': 'Name',
            'category__name': 'Category',
            'height': 'Height',
            'bust_size': 'Bust Size',
            'hip_size': 'Hip Size',
            'waist_size': 'Waist Size',
            'shoe_size': 'Shoe Size',
            'eye_color': 'Eye Color',
            'hair_color': 'Hair Color',
        }
        context['query'] = query
        context['attribute'] = attribute
        context['attribute_label'] = attribute_labels.get(attribute, attribute.title())
        return context
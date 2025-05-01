from sobaka.models import Human
from django.views.generic import ListView

class SearchResultsListView(ListView):
    model = Human
    context_object_name = 'humans_list'
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        attribute = self.request.GET.get('attribute', 'name')

        valid_attributes = [
            'name', 'height', 'bust_size', 'hip_size',
            'waist_size', 'shoe_size', 'eye_color', 'hair_color'
        ]

        if not query or attribute not in valid_attributes:
            return Human.objects.none()

        if attribute in ['height', 'bust_size', 'hip_size', 'waist_size', 'shoe_size']:
            filter_kwargs = {f"{attribute}__exact": query}
        else:
            filter_kwargs = {f"{attribute}__icontains": query}

        return Human.objects.filter(**filter_kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        attribute = self.request.GET.get('attribute', 'name')

        attribute_labels = {
            'name': 'Name',
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
from django.shortcuts import render, get_object_or_404
from .models import Category, Human
from django.core.paginator import Paginator, EmptyPage, InvalidPage

def hum_list(request, category_id=None):
    category = None
    humans = Human.objects.filter(available=True)

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        humans = Human.objects.filter(category=category, available=True)

    paginator = Paginator(humans, 6)  # Set the number of items per page
    try:
        page = int(request.GET.get('page', '1'))  # Get the current page number
    except ValueError:
        page = 1  # Default to page 1 if the page parameter is invalid
    try:
        humans = paginator.page(page)  # Get the humans for the current page
    except (EmptyPage, InvalidPage):
        humans = paginator.page(paginator.num_pages)  # Show the last page if the page is out of range

    return render(request, 'sobaka/category.html', {
        'category': category,
        'hums': humans,
        'page': page,  # Pass the current page to the template
    })
    

def human_detail(request, category_id, human_id):
    human = get_object_or_404(Human, category_id=category_id, id=human_id)
    return render(request, 'sobaka/human.html', {'human':human})
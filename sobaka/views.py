from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Human, Review
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from order.models import OrderItem
from .forms import ReviewForm

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

@login_required
def leave_review(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id, order__emailAddress=request.user.email)
    human = get_object_or_404(Human, name=order_item.product)

    if order_item.reviewed:
        return redirect(human.get_absolute_url())  # Redirect if already reviewed

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.human = human
            review.user = request.user
            review.save()
            order_item.reviewed = True
            order_item.save()
            return redirect(human.get_absolute_url())
    else:
        form = ReviewForm()

    return render(request, 'sobaka/leave_review.html', {'form': form, 'human': human})
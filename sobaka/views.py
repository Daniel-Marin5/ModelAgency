from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Category, Human, Review, NewsArticle
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from order.models import OrderItem
from .forms import ReviewForm, HumanForm, NewsArticleForm
from django.core.paginator import Paginator

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

def news_list(request):
    articles = NewsArticle.objects.all()
    return render(request, 'sobaka/news.html', {'articles': articles})
    

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

def is_admin(user):
    return user.is_authenticated and user.permissions

@user_passes_test(is_admin)
def add_human(request):
    if request.method == 'POST':
        form = HumanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = HumanForm()
    return render(request, 'sobaka/add_human.html', {'form': form})

@user_passes_test(is_admin)
def edit_human(request, human_id):
    human = get_object_or_404(Human, id=human_id)
    if request.method == 'POST':
        form = HumanForm(request.POST, request.FILES, instance=human)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = HumanForm(instance=human)
    return render(request, 'sobaka/edit_human.html', {'form': form, 'human': human})

@user_passes_test(is_admin)
def delete_human(request, human_id):
    human = get_object_or_404(Human, id=human_id)
    if request.method == 'POST':
        human.delete()
        return redirect('accounts:profile')
    return render(request, 'sobaka/delete_human.html', {'human': human})

@user_passes_test(is_admin)
def add_news_article(request):
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = NewsArticleForm()
    return render(request, 'sobaka/add_news_article.html', {'form': form})


@user_passes_test(is_admin)
def edit_news_article(request, article_id):
    article = get_object_or_404(NewsArticle, id=article_id)
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = NewsArticleForm(instance=article)
    return render(request, 'sobaka/edit_news_article.html', {'form': form, 'article': article})


@user_passes_test(is_admin)
def delete_news_article(request, article_id):
    article = get_object_or_404(NewsArticle, id=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('accounts:profile')
    return render(request, 'sobaka/delete_news_article.html', {'article': article})

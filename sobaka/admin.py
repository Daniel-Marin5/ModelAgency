from django.contrib import admin
from .models import Category, Human, UnavailableDate, Review, NewsArticle

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)

class HumanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'available','height', 'shoe_size', 'waist_size', 'bust_size', 'hip_size', 'eye_color', 'hair_color']
    list_editable = ['price', 'available']
    list_per_page = 20

admin.site.register(Human, HumanAdmin)

class UnavailableDateAdmin(admin.ModelAdmin):
    list_display = ['human', 'date']
    list_editable = ['date']

admin.site.register(UnavailableDate, UnavailableDateAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['human', 'user', 'rating', 'created']
    list_filter = ['rating', 'created']
    search_fields = ['human__name', 'user__username', 'comment']

admin.site.register(Review, ReviewAdmin)

class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    search_fields = ['title']
    list_filter = ['created']

admin.site.register(NewsArticle, NewsArticleAdmin)
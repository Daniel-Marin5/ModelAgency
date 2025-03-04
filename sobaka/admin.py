from django.contrib import admin
from .models import Category, Human

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)

class HumanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'category', 'available',]
    list_editable = ['price', 'available']
    list_per_page = 20

admin.site.register(Human, HumanAdmin)
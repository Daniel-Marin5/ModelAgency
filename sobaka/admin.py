from django.contrib import admin
from .models import Category, Human

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)

class HumanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'available','height', 'shoe_size', 'waist_size', 'bust_size', 'hip_size', 'eye_color', 'hair_color']
    list_editable = ['price', 'available']
    list_per_page = 20

admin.site.register(Human, HumanAdmin)
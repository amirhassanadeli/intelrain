# admin.py
from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_category_display', 'icon', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {}  # No slug needed
    fields = ['title', 'icon', 'category', 'description', 'features', 'is_active']
    
    def get_category_display(self, obj):
        return obj.get_category_display()
    get_category_display.short_description = 'Category'
# portfolio/admin.py
from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'icon', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    fields = [
        'title', 'category', 'icon', 'description', 
        'results', 'tech', 'client_name', 'completion_date', 'is_active'
    ]
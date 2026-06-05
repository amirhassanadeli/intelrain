# portfolio/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Project
from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectCreateUpdateSerializer
)

class ProjectListView(generics.ListCreateAPIView):
    """لیست همه پروژه‌ها یا ساخت پروژه جدید"""
    queryset = Project.objects.filter(is_active=True)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectCreateUpdateSerializer
        return ProjectListSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        detail_serializer = ProjectDetailSerializer(serializer.instance)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """دریافت پروژه با هش و اسلاگ"""
    
    def get_object(self):
        hash_str = self.kwargs.get('hash')
        slug = self.kwargs.get('slug')
        
        project = Project.get_by_hash(hash_str)
        
        if not project or project.slug != slug or not project.is_active:
            from rest_framework.exceptions import NotFound
            raise NotFound("Project not found")
        
        return project
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProjectCreateUpdateSerializer
        return ProjectDetailSerializer


@api_view(['GET'])
def projects_by_category(request):
    """گرفتن پروژه‌ها بر اساس دسته‌بندی"""
    categories = {}
    for category_code, category_name in Project.CATEGORY_CHOICES:
        projects = Project.objects.filter(category=category_code, is_active=True)
        if projects.exists():
            categories[category_code] = {
                'category': category_code,
                'category_display': category_name,
                'projects': ProjectListSerializer(projects, many=True).data
            }
    
    return Response(list(categories.values()))
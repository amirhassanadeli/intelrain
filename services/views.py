# services/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from .models import Service
from .serializers import (
    ServiceListSerializer,
    ServiceDetailSerializer,
    ServiceCreateUpdateSerializer,
    ServiceByCategorySerializer
)

class ServiceListView(generics.ListCreateAPIView):
    """لیست همه سرویس‌ها یا ساخت سرویس جدید"""
    queryset = Service.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ServiceCreateUpdateSerializer
        return ServiceListSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        detail_serializer = ServiceDetailSerializer(serializer.instance)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ServiceDetailSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        hash_str = self.kwargs.get('hash')
        slug = self.kwargs.get('slug')
        
        # پیدا کردن سرویس با هش
        service = Service.get_by_hash(hash_str)
        
        # بررسی وجود سرویس و مطابقت slug
        if not service or service.slug != slug or not service.is_active:
            from rest_framework.exceptions import NotFound
            raise NotFound("Service not found")
        
        return service
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ServiceCreateUpdateSerializer
        return ServiceDetailSerializer


@api_view(['GET'])
def services_by_category(request):

    categories = {}
    for category_code, category_name in Service.CATEGORY_CHOICES:
        services = Service.objects.filter(category=category_code, is_active=True)
        if services.exists():
            categories[category_code] = {
                'category': category_code,
                'category_display': category_name,
                'services': ServiceListSerializer(services, many=True).data
            }
    
    serializer = ServiceByCategorySerializer(list(categories.values()), many=True)
    return Response(serializer.data)
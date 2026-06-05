# services/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # لیست و ساخت سرویس جدید
    path('', views.ServiceListView.as_view(), name='service-list'),
    
    # دسته‌بندی
    path('by-category/', views.services_by_category, name='services-by-category'),
    
    # جزئیات سرویس با هش و اسلاگ
    path('<str:hash>/<slug:slug>/', views.ServiceDetailView.as_view(), name='service-detail'),
]
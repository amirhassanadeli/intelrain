# portfolio/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('<str:hash>/<slug:slug>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('by-category/', views.projects_by_category, name='projects-by-category'),
]
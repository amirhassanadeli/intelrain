from django.urls import path
from . import views

# contact/urls.py
urlpatterns = [
    path('csrf/', views.get_csrf_token, name='csrf'),
    path('submit/', views.ContactCreateView.as_view(), name='contact-submit'),
]
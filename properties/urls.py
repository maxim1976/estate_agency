from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('agents/', views.agent_list, name='agent_list'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
]

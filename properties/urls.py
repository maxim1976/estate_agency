from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('agents/', views.agent_list, name='agent_list'),
    path('agents/<int:pk>/', views.agent_profile, name='agent_profile'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('register/', views.agent_register, name='agent_register'),
    path('login/', views.agent_login, name='agent_login'),
    path('logout/', views.agent_logout, name='agent_logout'),
    
    # Agent dashboard and property management
    path('dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('properties/create/', views.property_create, name='property_create'),
    path('properties/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('properties/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('property-images/<int:pk>/delete/', views.property_image_delete, name='property_image_delete'),
]

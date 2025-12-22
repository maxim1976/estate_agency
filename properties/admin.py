from django.contrib import admin
from .models import Agent, Property, PropertyImage, Contact


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'specialization']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'price', 'status', 'bedrooms', 'bathrooms', 'agent', 'featured', 'created_at']
    list_filter = ['status', 'property_type', 'featured', 'city']
    search_fields = ['title', 'address', 'description']
    list_editable = ['status', 'featured']
    inlines = [PropertyImageInline]
    date_hierarchy = 'created_at'


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'is_primary', 'order']
    list_filter = ['is_primary']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'property', 'created_at', 'responded']
    list_filter = ['responded', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    list_editable = ['responded']
    readonly_fields = ['created_at']

from django.contrib import admin
from .models import Agent, Property, PropertyImage, Contact, Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'tagline', 'logo', 'hero_image')
        }),
        ('About Us', {
            'fields': ('story', 'mission', 'vision'),
            'description': 'Tell your company story and values'
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address', 'city', 'state', 'postal_code', 'country', 'business_hours')
        }),
        ('Office Location', {
            'fields': ('office_latitude', 'office_longitude'),
            'description': 'Add coordinates for map display on contact page'
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('founded_year', 'years_of_experience', 'total_properties_sold', 'happy_clients'),
            'description': 'Display impressive statistics on your site'
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Only allow one Company instance"""
        return not Company.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Don't allow deletion of Company instance"""
        return False


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'specialization', 'is_authorized']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    list_filter = ['is_authorized']
    list_editable = ['is_authorized']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'price', 'status', 'bedrooms', 'bathrooms', 'agent', 'featured', 'created_at']
    list_filter = ['status', 'property_type', 'featured', 'city']
    search_fields = ['title', 'address', 'description']
    list_editable = ['status', 'featured']
    inlines = [PropertyImageInline]
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'price', 'listing_type', 'property_type', 'status', 'featured')
        }),
        ('Location', {
            'fields': ('address', 'city', 'postal_code', 'latitude', 'longitude'),
            'description': 'Enter latitude and longitude for map display. You can find coordinates on Google Maps by right-clicking a location.'
        }),
        ('Property Details', {
            'fields': ('bedrooms', 'bathrooms', 'area_sqm', 'year_built', 'parking_spaces')
        }),
        ('Agent', {
            'fields': ('agent',)
        }),
    )


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

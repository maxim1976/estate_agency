from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Company(models.Model):
    """
    Company information - Should only have one instance.
    Stores all information about the real estate agency.
    """
    name = models.CharField(max_length=200, default='Prime Estate Agency')
    tagline = models.CharField(max_length=255, blank=True, help_text='Short catchy phrase (e.g., "Your Dream Home Awaits")')
    
    # Images
    logo = models.ImageField(upload_to='company/', blank=True, null=True, help_text='Company logo')
    hero_image = models.ImageField(upload_to='company/', blank=True, null=True, help_text='Main hero/banner image for homepage and about page')
    
    # About/Story
    story = models.TextField(blank=True, help_text='Company story and background')
    mission = models.TextField(blank=True, help_text='Mission statement')
    vision = models.TextField(blank=True, help_text='Vision statement')
    
    # Contact Information
    email = models.EmailField(default='hello@primeestate.com')
    phone = models.CharField(max_length=20, default='+1 (555) 000-0000')
    address = models.CharField(max_length=255, default='123 Market Street, Suite 400')
    city = models.CharField(max_length=100, default='Cityville')
    state = models.CharField(max_length=100, default='ST')
    postal_code = models.CharField(max_length=10, default='12345')
    country = models.CharField(max_length=100, default='USA')
    
    # Office Location Coordinates
    office_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, help_text='Office latitude for map display')
    office_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, help_text='Office longitude for map display')
    
    # Business Hours
    business_hours = models.TextField(default='Mon-Fri: 9:00 AM - 6:00 PM\nSat: 10:00 AM - 4:00 PM\nSun: Closed')
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Additional Information
    founded_year = models.PositiveIntegerField(blank=True, null=True, help_text='Year the company was founded')
    total_properties_sold = models.PositiveIntegerField(default=0, help_text='Total properties sold (for statistics)')
    years_of_experience = models.PositiveIntegerField(default=10, help_text='Years of experience (for statistics)')
    happy_clients = models.PositiveIntegerField(default=500, help_text='Number of happy clients (for statistics)')
    
    # SEO
    meta_description = models.TextField(max_length=160, blank=True, help_text='SEO meta description for homepage')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Company Information'
        verbose_name_plural = 'Company Information'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Ensure only one Company instance exists"""
        if not self.pk and Company.objects.exists():
            raise ValidationError('Only one Company instance is allowed. Please edit the existing one.')
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        """Get or create the single Company instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='agents/', blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True)
    is_authorized = models.BooleanField(default=False, help_text='Agent must be authorized by admin to manage properties')
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"


class Property(models.Model):
    STATUS_CHOICES = [
        ('available', '可售 / Available'),
        ('pending', '待處理 / Pending'),
        ('sold', '已售出 / Sold'),
    ]
    
    TYPE_CHOICES = [
        ('house', '獨棟房屋 / House'),
        ('apartment', '公寓 / Apartment'),
        ('condo', '共管公寓 / Condo'),
        ('villa', '別墅 / Villa'),
        ('land', '土地 / Land'),
    ]
    
    LISTING_TYPE_CHOICES = [
        ('sale', '出售 / For Sale'),
        ('rent', '出租 / For Rent'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, default='sale')
    property_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, default='Hualien')
    postal_code = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, help_text='Latitude coordinate for map display')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, help_text='Longitude coordinate for map display')
    
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    area_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    
    year_built = models.PositiveIntegerField(blank=True, null=True)
    parking_spaces = models.PositiveIntegerField(default=0)
    
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, related_name='properties')
    
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-is_primary']
    
    def __str__(self):
        return f"{self.property.title} - Image {self.order}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Contact from {self.name} - {self.created_at.strftime('%Y-%m-%d')}"

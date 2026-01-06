from django import forms
from .models import Property, PropertyImage


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'price', 'listing_type', 'property_type', 'status',
            'address', 'city', 'postal_code', 'latitude', 'longitude',
            'bedrooms', 'bathrooms', 'area_sqm', 'year_built', 'parking_spaces'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
            'listing_type': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
            'property_type': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
            'status': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
            'address': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
            'postal_code': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
            'latitude': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary', 'step': 'any'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
            'area_sqm': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary', 'step': '0.01'}),
            'year_built': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
            'parking_spaces': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
        }


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption', 'is_primary', 'order']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-surface-dark text-text-main-light dark:text-text-main-dark focus:ring-2 focus:ring-primary'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'h-5 w-5 rounded border-gray-300 text-primary focus:ring-primary'}),
        }

from django.conf import settings
from .models import Company


def google_maps_api_key(request):
    """Make Google Maps API key available in all templates"""
    return {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }


def company_info(request):
    """Make company information available in all templates"""
    try:
        company = Company.get_instance()
    except:
        company = None
    
    return {
        'company': company
    }

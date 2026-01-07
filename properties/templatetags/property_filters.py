from django import template

register = template.Library()

@register.filter
def sqm_to_sqft(value):
    """Convert square meters to square feet"""
    try:
        return int(float(value) * 10.764)
    except (ValueError, TypeError):
        return 0

@register.filter
def format_price(value):
    """Format price with commas"""
    try:
        return "{:,.0f}".format(float(value))
    except (ValueError, TypeError):
        return "0"

@register.filter
def get_listing_badge(listing_type):
    """Get badge color for listing type"""
    if listing_type == 'sale':
        return 'bg-green-500'
    elif listing_type == 'rent':
        return 'bg-blue-500'
    return 'bg-gray-500'

@register.filter
def get_listing_text(listing_type):
    """Get text for listing type"""
    if listing_type == 'sale':
        return 'FOR SALE / 出售'
    elif listing_type == 'rent':
        return 'FOR RENT / 蒩蒩'
    return 'AVAILABLE'

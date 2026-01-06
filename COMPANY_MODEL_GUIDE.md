# Company Model - Quick Reference

## ✅ What Was Added

A comprehensive `Company` model has been added to store all your real estate agency information in the database.

## 📋 Fields Included

### Basic Information
- **name**: Company name (default: "Prime Estate Agency")
- **tagline**: Short catchphrase
- **logo**: Company logo image
- **hero_image**: Main hero/banner image

### About Section
- **story**: Company history and background
- **mission**: Mission statement
- **vision**: Vision statement

### Contact Information
- **email**: Contact email
- **phone**: Phone number
- **address**: Street address
- **city**: City name
- **state**: State/Province
- **postal_code**: ZIP/Postal code
- **country**: Country name
- **business_hours**: Operating hours (multi-line text)

### Office Location
- **office_latitude**: Coordinates for map
- **office_longitude**: Coordinates for map

### Social Media
- **facebook_url**
- **twitter_url**
- **instagram_url**
- **linkedin_url**
- **youtube_url**

### Statistics (for homepage)
- **founded_year**: Year established
- **years_of_experience**: Years in business
- **total_properties_sold**: Number of properties sold
- **happy_clients**: Number of satisfied clients

### SEO
- **meta_description**: Homepage meta description

## 🎯 How to Use

### 1. Access in Admin

Go to: **http://127.0.0.1:8000/admin/properties/company/**

- Only ONE company instance is allowed (singleton pattern)
- Cannot be deleted (protection enabled)
- All organized in clean fieldsets

### 2. Add Your Information

Simply fill in the fields in the Django admin:
1. Basic info (name, logo, hero image)
2. Your company story
3. Contact details
4. Office coordinates (find on Google Maps)
5. Social media links
6. Statistics for impressive numbers

### 3. Access in Templates

The company information is automatically available in ALL templates via context processor:

```django
{# Company name #}
{{ company.name }}

{# Contact information #}
{{ company.email }}
{{ company.phone }}
{{ company.address }}

{# Office location for maps #}
{{ company.office_latitude }}
{{ company.office_longitude }}

{# Social media #}
{% if company.facebook_url %}
    <a href="{{ company.facebook_url }}">Facebook</a>
{% endif %}

{# Statistics #}
<p>{{ company.years_of_experience }}+ Years of Experience</p>
<p>{{ company.total_properties_sold }}+ Properties Sold</p>
<p>{{ company.happy_clients }}+ Happy Clients</p>

{# Hero image #}
{% if company.hero_image %}
    <img src="{{ company.hero_image.url }}" alt="{{ company.name }}">
{% endif %}
```

### 4. Already Integrated

The **Contacts page** now automatically uses:
- ✅ Company address
- ✅ Company phone
- ✅ Company email
- ✅ Company office coordinates (for map)
- ✅ Business hours

## 📍 Setting Office Location

1. Go to [Google Maps](https://www.google.com/maps)
2. Find your office location
3. Right-click → Copy coordinates
4. Paste into `office_latitude` and `office_longitude` fields in admin
5. The map on the contacts page will automatically update!

## 🎨 Using on Other Pages

### Homepage Hero Section
```django
{% if company.hero_image %}
    <div style="background-image: url('{{ company.hero_image.url }}')">
        <h1>{{ company.name }}</h1>
        <p>{{ company.tagline }}</p>
    </div>
{% endif %}
```

### About Page
```django
<h1>About {{ company.name }}</h1>

<h2>Our Story</h2>
<p>{{ company.story|linebreaks }}</p>

<h2>Our Mission</h2>
<p>{{ company.mission|linebreaks }}</p>

<h2>Our Vision</h2>
<p>{{ company.vision|linebreaks }}</p>

<div class="stats">
    <div>{{ company.years_of_experience }}+ Years</div>
    <div>{{ company.total_properties_sold }}+ Properties</div>
    <div>{{ company.happy_clients }}+ Clients</div>
</div>
```

### Footer
```django
<footer>
    <div>
        {% if company.logo %}
            <img src="{{ company.logo.url }}" alt="{{ company.name }}">
        {% endif %}
        <p>{{ company.tagline }}</p>
    </div>
    
    <div>
        <h3>Contact</h3>
        <p>{{ company.address }}</p>
        <p>{{ company.city }}, {{ company.state }} {{ company.postal_code }}</p>
        <p>{{ company.phone }}</p>
        <p>{{ company.email }}</p>
    </div>
    
    <div>
        <h3>Follow Us</h3>
        {% if company.facebook_url %}<a href="{{ company.facebook_url }}">Facebook</a>{% endif %}
        {% if company.twitter_url %}<a href="{{ company.twitter_url }}">Twitter</a>{% endif %}
        {% if company.instagram_url %}<a href="{{ company.instagram_url }}">Instagram</a>{% endif %}
        {% if company.linkedin_url %}<a href="{{ company.linkedin_url }}">LinkedIn</a>{% endif %}
    </div>
</footer>
```

## 🔒 Security Features

- **Singleton Pattern**: Only ONE company instance allowed
- **Cannot be deleted**: Protection prevents accidental deletion
- **Automatic creation**: `Company.get_instance()` creates if doesn't exist

## 🚀 Next Steps

1. **Fill in company information** in admin
2. **Add office coordinates** for map display
3. **Upload logo and hero image**
4. **Update about page** to use company model
5. **Add social media links** to footer
6. **Display statistics** on homepage

## 💡 Pro Tips

- Use high-quality images for logo and hero_image
- Keep tagline short and memorable (under 60 characters)
- Story should be personal and engaging
- Update statistics regularly to stay current
- Business hours support multi-line text (use Shift+Enter)
- Test all social media links before publishing

Server running at: **http://127.0.0.1:8000/**
Admin at: **http://127.0.0.1:8000/admin/**

The company model is now ready to use! 🎉

# Django Template Structure Documentation

## Base Template (`templates/base.html`)

### Overview
The base template provides the foundational HTML structure that all other templates inherit from. It follows Django best practices for template inheritance and organization.

### Structure

```html
<!DOCTYPE html>
<html class="light" lang="en">
<head>
    <!-- Meta tags and title -->
    <!-- Fonts: Inter, Material Symbols -->
    <!-- Tailwind CSS with custom configuration -->
    <!-- Custom styles -->
    <!-- Block for additional CSS -->
</head>
<body>
    <div class="wrapper">
        <!-- Header include -->
        <!-- Content block -->
        <!-- Footer include -->
    </div>
    <!-- Block for additional JS -->
</body>
</html>
```

### Key Features

#### 1. **Template Blocks**
- `{% block title %}` - Page title (default: "EstateAgency - Find Your Dream Home")
- `{% block extra_css %}` - Additional CSS for specific pages
- `{% block content %}` - Main page content
- `{% block extra_js %}` - Additional JavaScript for specific pages

#### 2. **Includes**
- `{% include 'includes/_header.html' %}` - Navigation header
- `{% include 'includes/_footer.html' %}` - Footer with links

#### 3. **Styling System**

**Tailwind CSS Configuration:**
```javascript
colors: {
    "primary": "#1754cf",                    // Brand blue
    "background-light": "#f6f6f8",          // Light mode background
    "background-dark": "#111621",           // Dark mode background
    "surface-light": "#ffffff",             // Cards/surfaces (light)
    "surface-dark": "#1a2231",             // Cards/surfaces (dark)
    "text-main-light": "#111318",          // Main text (light)
    "text-main-dark": "#f0f2f4",           // Main text (dark)
    "text-secondary-light": "#636f88",     // Secondary text (light)
    "text-secondary-dark": "#9ba6b8",      // Secondary text (dark)
    "border-light": "#dcdfe5",             // Borders (light)
    "border-dark": "#2d3748",              // Borders (dark)
}
```

**Font System:**
- Primary: Inter (400, 500, 700, 900 weights)
- Icons: Material Symbols Outlined

**Dark Mode:**
- Configured via `darkMode: "class"`
- Toggle by adding `dark` class to `<html>` element

### Usage Examples

#### Basic Page Template
```django
{% extends 'base.html' %}

{% block title %}My Page Title{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    <h1>Page Content</h1>
</div>
{% endblock %}
```

#### Page with Extra CSS
```django
{% extends 'base.html' %}

{% block extra_css %}
<style>
    .custom-style {
        /* Custom styles */
    }
</style>
{% endblock %}

{% block content %}
<!-- Page content -->
{% endblock %}
```

#### Page with Extra JavaScript
```django
{% extends 'base.html' %}

{% block content %}
<!-- Page content -->
{% endblock %}

{% block extra_js %}
<script>
    // Custom JavaScript
    console.log('Page loaded');
</script>
{% endblock %}
```

## Includes

### Header (`templates/includes/_header.html`)

**Features:**
- Sticky navigation bar
- Logo and brand name
- Navigation links (Buy, Rent, Sell, Agents, About)
- User authentication status (Admin/Login button)
- Contact Us CTA button
- Responsive design (mobile menu hidden on small screens)

**Dynamic URLs:**
```django
{% url 'properties:home' %}
{% url 'properties:property_list' %}
{% url 'properties:agent_list' %}
{% url 'properties:about' %}
{% url 'properties:contacts' %}
{% url 'admin:index' %}
{% url 'admin:login' %}
```

### Footer (`templates/includes/_footer.html`)

**Sections:**
1. **Brand Column** - Logo, description, social links
2. **Company Links** - About, Agents, Contact
3. **Resources** - Browse Properties, Featured Listings
4. **Newsletter** - Email subscription form

**Features:**
- Dynamic year with `{% now "Y" %}`
- CSRF protection on forms with `{% csrf_token %}`
- Responsive grid layout
- Social media icons (Facebook, Twitter, Instagram)

## App Templates (`templates/properties/`)

### Home Page (`home.html`)
**Extends:** `base.html`

**Sections:**
- Hero section with search form
- Featured properties grid (dynamic with Django for loop)
- Value proposition cards
- Call-to-action section

**Dynamic Content:**
```django
{% for property in featured_properties %}
    <!-- Property card -->
    {{ property.title }}
    {{ property.price|floatformat:0 }}
    {{ property.address }}, {{ property.city }}
    {{ property.bedrooms }} Beds
    {{ property.bathrooms }} Baths
    {{ property.area_sqm|floatformat:0 }} m²
{% empty %}
    <!-- No properties message -->
{% endfor %}
```

### Best Practices Applied

1. **DRY (Don't Repeat Yourself)**
   - Common HTML structure in base.html
   - Reusable components in includes/
   - Template inheritance reduces duplication

2. **SEO Optimization**
   - Proper `<title>` tags per page
   - Semantic HTML structure
   - Meta viewport for mobile responsiveness

3. **Accessibility**
   - Semantic HTML elements
   - ARIA labels on icon links
   - Proper heading hierarchy

4. **Performance**
   - External CSS/JS from CDN
   - Minimal inline styles
   - Lazy loading support ready

5. **Maintainability**
   - Clear file organization
   - Descriptive block names
   - Consistent naming conventions

## File Organization

```
templates/
├── base.html                  # Main layout template
├── includes/                  # Reusable components
│   ├── _header.html          # Navigation header
│   └── _footer.html          # Site footer
└── properties/               # App-specific templates
    ├── home.html             # Homepage
    ├── property_list.html    # Property listing page
    ├── property_detail.html  # Single property page
    ├── agent.html            # Agent directory
    ├── contacts.html         # Contact form
    └── about.html            # About page
```

## Customization Guide

### Adding a New Page

1. Create new template in `templates/properties/`
2. Extend base template:
   ```django
   {% extends 'base.html' %}
   
   {% block title %}New Page{% endblock %}
   
   {% block content %}
   <!-- Your content -->
   {% endblock %}
   ```
3. Add view in `properties/views.py`
4. Add URL pattern in `properties/urls.py`

### Modifying Colors

Edit Tailwind config in `base.html`:
```javascript
colors: {
    "primary": "#YOUR_COLOR",
    // Other colors...
}
```

### Adding Navigation Link

Edit `templates/includes/_header.html`:
```html
<a class="text-sm font-medium hover:text-primary transition-colors" 
   href="{% url 'properties:your_view' %}">
   New Link
</a>
```

## Notes

- All PNG files in templates folder are design mockups (not used in production)
- Old template backed up as `home_old.html` for reference
- Dark mode toggle functionality can be added with JavaScript
- Search form in hero submits to property_list view with GET parameters

---

**Created:** December 22, 2025  
**Django Version:** 6.0  
**Tailwind CSS:** via CDN  
**Python Version:** 3.13+

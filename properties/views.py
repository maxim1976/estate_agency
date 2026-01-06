from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import models
from .models import Property, Agent, Contact, PropertyImage
from .forms import PropertyForm, PropertyImageForm


def home(request):
    featured_properties = Property.objects.filter(featured=True, status='available')[:6]
    context = {
        'featured_properties': featured_properties,
    }
    return render(request, 'properties/home.html', context)


def property_list(request):
    properties = Property.objects.filter(status='available')
    
    listing_type = request.GET.get('listing_type')
    property_type = request.GET.get('property_type')
    location = request.GET.get('location')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')
    sort_by = request.GET.get('sort_by', 'newest')
    
    if listing_type:
        properties = properties.filter(listing_type=listing_type)
    
    # Handle multiple property types
    if property_type:
        property_types = property_type.split(',')
        properties = properties.filter(property_type__in=property_types)
    
    if location:
        properties = properties.filter(
            models.Q(city__icontains=location) | 
            models.Q(address__icontains=location) |
            models.Q(postal_code__icontains=location)
        )
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if bedrooms:
        properties = properties.filter(bedrooms__gte=bedrooms)
    if bathrooms:
        properties = properties.filter(bathrooms__gte=bathrooms)
    
    # Apply sorting
    if sort_by == 'price_low':
        properties = properties.order_by('price')
    elif sort_by == 'price_high':
        properties = properties.order_by('-price')
    elif sort_by == 'sqft':
        properties = properties.order_by('-area_sqm')
    else:  # newest
        properties = properties.order_by('-created_at')
    
    paginator = Paginator(properties, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'properties': page_obj,
        'page_obj': page_obj,
        'current_sort': sort_by,
    }
    return render(request, 'properties/property_list.html', context)


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    context = {
        'property': property,
    }
    return render(request, 'properties/property_detail.html', context)


def agent_list(request):
    agents = Agent.objects.all()
    context = {
        'agents': agents,
    }
    return render(request, 'properties/agent_list.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        property_id = request.POST.get('property_id')
        
        contact = Contact(
            name=name,
            email=email,
            phone=phone,
            message=message,
        )
        
        if property_id:
            contact.property_id = property_id
        
        contact.save()
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contacts')
    
    return render(request, 'properties/contacts.html')


def about(request):
    agents = Agent.objects.all()
    context = {
        'agents': agents,
    }
    return render(request, 'properties/about.html', context)


def agent_register(request):
    if request.user.is_authenticated:
        return redirect('properties:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        specialization = request.POST.get('specialization', '')
        bio = request.POST.get('bio', '')
        
        # Validation
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'properties/agent_register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'properties/agent_register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'properties/agent_register.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create agent profile
        agent = Agent.objects.create(
            user=user,
            phone=phone,
            specialization=specialization,
            bio=bio
        )
        
        if 'photo' in request.FILES:
            agent.photo = request.FILES['photo']
            agent.save()
        
        messages.success(request, 'Registration successful! You can now login.')
        return redirect('properties:agent_login')
    
    return render(request, 'properties/agent_register.html')


def agent_login(request):
    if request.user.is_authenticated:
        return redirect('properties:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            next_url = request.GET.get('next', 'properties:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'properties/agent_login.html')


def agent_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('properties:home')


def agent_profile(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    agent_properties = Property.objects.filter(agent=agent, status='available').order_by('-created_at')
    
    # Calculate stats
    total_properties = agent_properties.count()
    sold_properties = Property.objects.filter(agent=agent, status='sold').count()
    
    context = {
        'agent': agent,
        'properties': agent_properties,
        'total_properties': total_properties,
        'sold_properties': sold_properties,
    }
    return render(request, 'properties/agent_profile.html', context)


@login_required
def agent_dashboard(request):
    """Dashboard for agents to manage their properties"""
    try:
        agent = request.user.agent
    except Agent.DoesNotExist:
        messages.error(request, 'You need to be registered as an agent.')
        return redirect('properties:home')
    
    if not agent.is_authorized:
        messages.warning(request, 'Your agent account is pending authorization from admin.')
        return render(request, 'properties/agent_unauthorized.html', {'agent': agent})
    
    agent_properties = Property.objects.filter(agent=agent).order_by('-created_at')
    
    # Stats
    total_properties = agent_properties.count()
    available_properties = agent_properties.filter(status='available').count()
    pending_properties = agent_properties.filter(status='pending').count()
    sold_properties = agent_properties.filter(status='sold').count()
    
    context = {
        'agent': agent,
        'properties': agent_properties,
        'total_properties': total_properties,
        'available_properties': available_properties,
        'pending_properties': pending_properties,
        'sold_properties': sold_properties,
    }
    return render(request, 'properties/agent_dashboard.html', context)


@login_required
def property_create(request):
    """Create a new property"""
    try:
        agent = request.user.agent
    except Agent.DoesNotExist:
        messages.error(request, 'You need to be registered as an agent.')
        return redirect('properties:home')
    
    if not agent.is_authorized:
        messages.error(request, 'You are not authorized to create properties.')
        return redirect('properties:agent_dashboard')
    
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.agent = agent
            property.save()
            
            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for idx, image in enumerate(images):
                PropertyImage.objects.create(
                    property=property,
                    image=image,
                    order=idx,
                    is_primary=(idx == 0)
                )
            
            messages.success(request, 'Property created successfully!')
            return redirect('properties:agent_dashboard')
    else:
        form = PropertyForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    return render(request, 'properties/property_form.html', context)


@login_required
def property_edit(request, pk):
    """Edit an existing property"""
    property = get_object_or_404(Property, pk=pk)
    
    try:
        agent = request.user.agent
    except Agent.DoesNotExist:
        messages.error(request, 'You need to be registered as an agent.')
        return redirect('properties:home')
    
    if property.agent != agent:
        messages.error(request, 'You can only edit your own properties.')
        return redirect('properties:agent_dashboard')
    
    if not agent.is_authorized:
        messages.error(request, 'You are not authorized to edit properties.')
        return redirect('properties:agent_dashboard')
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            
            # Handle new image uploads
            images = request.FILES.getlist('images')
            if images:
                current_max_order = property.images.count()
                for idx, image in enumerate(images):
                    PropertyImage.objects.create(
                        property=property,
                        image=image,
                        order=current_max_order + idx,
                        is_primary=False
                    )
            
            messages.success(request, 'Property updated successfully!')
            return redirect('properties:agent_dashboard')
    else:
        form = PropertyForm(instance=property)
    
    context = {
        'form': form,
        'property': property,
        'action': 'Edit',
    }
    return render(request, 'properties/property_form.html', context)


@login_required
def property_delete(request, pk):
    """Delete a property"""
    property = get_object_or_404(Property, pk=pk)
    
    try:
        agent = request.user.agent
    except Agent.DoesNotExist:
        messages.error(request, 'You need to be registered as an agent.')
        return redirect('properties:home')
    
    if property.agent != agent:
        messages.error(request, 'You can only delete your own properties.')
        return redirect('properties:agent_dashboard')
    
    if not agent.is_authorized:
        messages.error(request, 'You are not authorized to delete properties.')
        return redirect('properties:agent_dashboard')
    
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('properties:agent_dashboard')
    
    context = {
        'property': property,
    }
    return render(request, 'properties/property_confirm_delete.html', context)


@login_required
def property_image_delete(request, pk):
    """Delete a property image"""
    image = get_object_or_404(PropertyImage, pk=pk)
    property = image.property
    
    try:
        agent = request.user.agent
    except Agent.DoesNotExist:
        messages.error(request, 'You need to be registered as an agent.')
        return redirect('properties:home')
    
    if property.agent != agent:
        messages.error(request, 'You can only delete images from your own properties.')
        return redirect('properties:agent_dashboard')
    
    if not agent.is_authorized:
        messages.error(request, 'You are not authorized to manage properties.')
        return redirect('properties:agent_dashboard')
    
    property_id = property.pk
    image.delete()
    messages.success(request, 'Image deleted successfully!')
    return redirect('properties:property_edit', pk=property_id)

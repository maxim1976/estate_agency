from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Property, Agent, Contact


def home(request):
    featured_properties = Property.objects.filter(featured=True, status='available')[:6]
    context = {
        'featured_properties': featured_properties,
    }
    return render(request, 'home.html', context)


def property_list(request):
    properties = Property.objects.filter(status='available')
    
    property_type = request.GET.get('type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bedrooms = request.GET.get('bedrooms')
    
    if property_type:
        properties = properties.filter(property_type=property_type)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if bedrooms:
        properties = properties.filter(bedrooms__gte=bedrooms)
    
    context = {
        'properties': properties,
    }
    return render(request, 'property_list.html', context)


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    context = {
        'property': property,
    }
    return render(request, 'property_detail.html', context)


def agent_list(request):
    agents = Agent.objects.all()
    context = {
        'agents': agents,
    }
    return render(request, 'agent.html', context)


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
    
    return render(request, 'contacts.html')


def about(request):
    agents = Agent.objects.all()
    context = {
        'agents': agents,
    }
    return render(request, 'about.html', context)

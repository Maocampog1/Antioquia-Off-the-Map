from .models import Municipality, Event, Activity, Restaurant, Accommodation, Category
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.conf import settings

# List of municipality names
def municipality_name_list(request):
    municipalities = Municipality.objects.all()
    return render(request, 'municipalities_name_list.html', {'municipalities': municipalities})

# Municipality detail by ID
def municipality_detail(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    accommodations = municipality.accommodations.all()
    restaurants = municipality.restaurants.all()
    activities = municipality.activities.all()

    return render(request, 'municipality_detail.html', {
        'municipality': municipality,
        'accommodations': accommodations,
        'restaurants': restaurants,
        'activities': activities,
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY
    })

# Municipality detail by name
def municipality_detail_by_name(request, municipality_name):
    municipality = get_object_or_404(Municipality, name=municipality_name)
    return render(request, 'municipality_detail.html', {'municipality': municipality})

# Real-time search without advanced filters
def search_municipalities(request):
    query = request.GET.get("q", "").strip()
    selected_location = request.GET.get("location", "").strip()
    selected_categories = request.GET.get("categories", "")
    
    # Convert categories to list of integers
    selected_categories = [int(c) for c in selected_categories.split(",") if c.isdigit()] if selected_categories else []

    # Apply filters
    municipalities = Municipality.objects.all()

    if query:
        municipalities = municipalities.filter(name__icontains=query)

    if selected_location:
        municipalities = municipalities.filter(location=selected_location)

    if selected_categories:
        municipalities = municipalities.filter(categories__id__in=selected_categories).distinct()

    # Optimized live search implementation
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        municipalities = municipalities.values("id", "name")  # Only return necessary fields
        return JsonResponse(list(municipalities), safe=False)

    # Redirect to detail page if only one municipality
    if municipalities.count() == 1:
        return redirect('municipality_detail', municipality_id=municipalities.first().id)

    # Show list of municipalities if multiple
    return render(request, 'municipality_list.html', {'municipalities': municipalities})

# Advanced search with filters and redirection if only one result
def filtered_search_municipalities(request):
    query = request.GET.get("q", "").strip()
    selected_location = request.GET.get("location", "").strip()
    selected_categories = request.GET.get("categories", "")

    # Convert categories to list of integers
    selected_categories = [int(c) for c in selected_categories.split(",") if c.isdigit()] if selected_categories else []

    # Apply filters
    municipalities = Municipality.objects.all()

    if query:
        municipalities = municipalities.filter(name__icontains=query)

    if selected_location:
        municipalities = municipalities.filter(location=selected_location)

    if selected_categories:
        municipalities = municipalities.filter(categories__id__in=selected_categories).distinct()

    # Redirect to detail page if only one result
    if municipalities.count() == 1:
        return redirect('municipality_detail', municipality_id=municipalities.first().id)

    # Show list if multiple results
    return render(request, 'municipality_list.html', {'municipalities': municipalities})

# Municipality event calendar
def event_calendar(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    events = municipality.events.all().order_by("date")  # Order events by date
    return render(request, "municipality_events.html", {"municipality": municipality, "events": events})

# Home page
def home(request):
    municipalities = Municipality.objects.all()
    categories = Category.objects.all()
    locations = Municipality.objects.values_list('location', flat=True).distinct()
    return render(request, 'home.html', {
        'municipalities': municipalities,
        'categories': categories,
        'locations': locations
    })

# Site base
def base(request):
    municipalities = Municipality.objects.all()
    categories = Category.objects.all()
    locations = Municipality.objects.values_list('location', flat=True).distinct()
    return render(request, 'base.html', {
        'municipalities': municipalities,
        'categories': categories,
        'locations': locations
    })

#FR10 Experience Search - Main Functions -->  
#Additionally, in the templates of destinations, an HTML file was created for this functionality, 
# as it was previously directing to another page of the web application. 

def experience_search_page(request):
    municipios = Municipality.objects.all()
    
    categorias = [
        {"value": "restaurants", "label": "Dónde comer"},
        {"value": "accommodations", "label": "Dónde dormir"},
        {"value": "activities", "label": "Qué hacer"},
    ]

    return render(request, 'experience_search.html', {
        "municipios": municipios,
        "categorias": categorias
    })

def search_experiences(request):
    municipality = request.GET.get("municipality1") 
    categories = request.GET.get("categories", "").split(",")

    # Create an empty dictionary to store results
    results = {
        "accommodations": [],
        "activities": [],
        "restaurants": []
    }

    if "accommodations" in categories:
        results["accommodations"] = list(
            Accommodation.objects.filter(municipality__name=municipality).values("name", "accommodation_type", "website")
        )

    if "activities" in categories:
        results["activities"] = list(
            Activity.objects.filter(municipality__name=municipality).values("name", "description")
        )

    if "restaurants" in categories:
        results["restaurants"] = list(
            Restaurant.objects.filter(municipality__name=municipality).values("name", "location", "cuisine_type")
        )

    return JsonResponse(results) 
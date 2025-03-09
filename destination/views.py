from .models import Municipality, Event, Category
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse


# Create your views here.
def municipality_name_list(request):
    municipalities = Municipality.objects.all()
    return render(request, 'municipalities_name_list.html', {'municipalities': municipalities})

def municipality_detail(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    return render(request, 'municipality_detail.html', {'municipality': municipality})

def municipality_detail_by_name(request, municipality_name):
    municipality = get_object_or_404(Municipality, name=municipality_name)
    return render(request, 'municipality_detail.html', {'municipality': municipality})

# View fot the municipality search in real time
def search_municipalities(request):
    query = request.GET.get("q", "").strip()
    selected_location = request.GET.get("location", "").strip()
    selected_categories = request.GET.getlist("categories") # Lista de categorías seleccionadas

    # Filtrar municipios según el nombre
    municipalities = Municipality.objects.all()
    
    if query:
        municipalities = municipalities.filter(name__icontains=query)

    # Filtrar por ubicación si se selecciona una
    if selected_location:
        municipalities = municipalities.filter(location=selected_location)

    # Filtrar por categorías si se seleccionan (asumiendo que Municipality tiene relación ManyToMany con Category)
    if selected_categories:
        municipalities = municipalities.filter(categories__id__in=selected_categories).distinct()

    # Retornar los municipios en formato JSON
    data = list(municipalities.values("id", "name"))
    return JsonResponse(data, safe=False)

def event_calendar(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    events = municipality.events.all().order_by("date")  # Obtain events ordered by date
    return render(request, "municipality_events.html", {"municipality": municipality, "events": events})

def home(request):
    municipalities = Municipality.objects.all()
    categories = Category.objects.all()
    locations = Municipality.objects.values_list('location', flat=True).distinct()
    return render(request, 'home.html', {
        'municipalities': municipalities,
        'categories': categories,
        'locations': locations
    })

def base(request):
    municipalities = Municipality.objects.all()
    categories = Category.objects.all()
    locations = Municipality.objects.values_list('location', flat=True).distinct()
    return render(request, 'base.html', {
        'municipalities': municipalities,
        'categories': categories,
        'locations': locations})

def municipality_detail(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    accommodations = municipality.accommodations.all()
    restaurants = municipality.restaurants.all()
    activities = municipality.activities.all()  # <-- Ahora también enviamos las actividades
    
    return render(request, 'municipality_detail.html', {
        'municipality': municipality,
        'accommodations': accommodations,
        'restaurants': restaurants,
        'activities': activities  # <-- Se envían al template
    })


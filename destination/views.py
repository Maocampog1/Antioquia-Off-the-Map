from .models import Municipality, Event
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Activity, Event, Restaurant, Accommodation

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


def event_calendar(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    events = municipality.events.all().order_by("date")  # Obtain events ordered by date
    return render(request, "municipality_events.html", {"municipality": municipality, "events": events})

def home(request):
    municipalities = Municipality.objects.all()
    return render(request, 'home.html', {'municipalities': municipalities})

def search_municipalities(request):
    query = request.GET.get("q", "").strip()
    if query:
        municipalities = Municipality.objects.filter(name__icontains=query).values("id", "name")
        return JsonResponse(list(municipalities), safe=False)
    return JsonResponse([], safe=False)

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


def experience_search_page(request):
    municipios = Municipality.objects.all()
    
    categorias = [
        {"value": "restaurants", "label": "Dónde comer", "count": Restaurant.objects.count()},
        {"value": "accommodations", "label": "Dónde dormir", "count": Accommodation.objects.count()},
        {"value": "activities", "label": "Qué hacer", "count": Activity.objects.count()},
    ]

    return render(request, 'experience_search.html', {
        "municipios": municipios,
        "categorias": categorias
    })

# def search_experiences(request):
#     municipio_id = request.GET.get("municipios")
#     categorias = request.GET.get("categorias", "").split(",")

#     experiencias = Experience.objects.filter(municipality_id=municipio_id)

#     if categorias and categorias != [""]:
#         experiencias = experiencias.filter(category__in=categorias)

#     experiencias_data = list(experiencias.values("id", "name", "municipality__name"))

#     return JsonResponse(experiencias_data, safe=False)

def search_experiences(request):
    municipality = request.GET.get("municipality1")  # ✅ Fixed case issue
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
    


from .models import Municipality, Event, Category
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.urls import reverse

# Lista de nombres de municipios
def municipality_name_list(request):
    municipalities = Municipality.objects.all()
    return render(request, 'municipalities_name_list.html', {'municipalities': municipalities})

# Detalle del municipio por ID
def municipality_detail(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    accommodations = municipality.accommodations.all()
    restaurants = municipality.restaurants.all()
    activities = municipality.activities.all()

    return render(request, 'municipality_detail.html', {
        'municipality': municipality,
        'accommodations': accommodations,
        'restaurants': restaurants,
        'activities': activities
    })

# Detalle del municipio por nombre
def municipality_detail_by_name(request, municipality_name):
    municipality = get_object_or_404(Municipality, name=municipality_name)
    return render(request, 'municipality_detail.html', {'municipality': municipality})

# Búsqueda en tiempo real sin filtros avanzados
def search_municipalities(request):
    query = request.GET.get("q", "").strip()
    selected_location = request.GET.get("location", "").strip()
    selected_categories = request.GET.get("categories", "")
    
    # Convertir categorías en lista de enteros
    selected_categories = [int(c) for c in selected_categories.split(",") if c.isdigit()] if selected_categories else []

    # Aplicar filtros
    municipalities = Municipality.objects.all()

    if query:
        municipalities = municipalities.filter(name__icontains=query)

    if selected_location:
        municipalities = municipalities.filter(location=selected_location)

    if selected_categories:
        municipalities = municipalities.filter(categories__id__in=selected_categories).distinct()

    # ✅ Implementación de búsqueda en vivo optimizada
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        municipalities = municipalities.values("id", "name")  # Solo devolver los campos necesarios
        return JsonResponse(list(municipalities), safe=False)

    # 🔄 Si hay solo un municipio, redirigir a su página de detalles
    if municipalities.count() == 1:
        return redirect('municipality_detail', municipality_id=municipalities.first().id)

    # 📄 Si hay varios, mostrar la lista de municipios
    return render(request, 'municipality_list.html', {'municipalities': municipalities})


# Búsqueda avanzada con filtros y redirección si hay un solo resultado
from django.shortcuts import render

def filtered_search_municipalities(request):
    query = request.GET.get("q", "").strip()
    selected_location = request.GET.get("location", "").strip()
    selected_categories = request.GET.get("categories", "")

    # Convertir categorías en lista de enteros
    selected_categories = [int(c) for c in selected_categories.split(",") if c.isdigit()] if selected_categories else []

    # Aplicar filtros
    municipalities = Municipality.objects.all()

    if query:
        municipalities = municipalities.filter(name__icontains=query)

    if selected_location:
        municipalities = municipalities.filter(location=selected_location)

    if selected_categories:
        municipalities = municipalities.filter(categories__id__in=selected_categories).distinct()

    # Si hay solo un resultado, redirigir a su página
    if municipalities.count() == 1:
        return redirect('municipality_detail', municipality_id=municipalities.first().id)

    # Si hay varios, mostrar la lista
    return render(request, 'municipality_list.html', {'municipalities': municipalities})



# Calendario de eventos del municipio
def event_calendar(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    events = municipality.events.all().order_by("date")  # Ordenar eventos por fecha
    return render(request, "municipality_events.html", {"municipality": municipality, "events": events})

# Página de inicio
def home(request):
    municipalities = Municipality.objects.all()
    categories = Category.objects.all()
    locations = Municipality.objects.values_list('location', flat=True).distinct()
    return render(request, 'home.html', {
        'municipalities': municipalities,
        'categories': categories,
        'locations': locations
    })

# Base del sitio
def base(request):
    municipalities = Municipality.objects.all()
    categories = Category.objects.all()
    locations = Municipality.objects.values_list('location', flat=True).distinct()
    return render(request, 'base.html', {
        'municipalities': municipalities,
        'categories': categories,
        'locations': locations
    })

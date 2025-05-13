from django.contrib.auth.decorators import login_required
from .models import Municipality, Event, Activity, Restaurant, Accommodation, Category, Toll, TravelerPost
from .forms import TravelerPostForm, ReviewForm
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
import json
import os
import re  # for regex validation of word characters

SEARCH_COUNT_PATH = os.path.join('destination/data', 'search_counts.json')

# List of municipality names
def municipality_name_list(request):
    municipalities = Municipality.objects.all()
    return render(request, 'municipalities_name_list.html', {'municipalities': municipalities})

# Municipality detail by ID
def municipality_detail(request, municipality_id):
    # 1. Obtener datos base
    municipality = get_object_or_404(Municipality, id=municipality_id)
    accommodations = municipality.accommodations.all()
    restaurants = municipality.restaurants.all()
    activities = municipality.activities.all()
    toll = municipality.tolls.all()
    reviews = municipality.reviews.all().order_by('-created_at')
    
    # 2. Lista de palabras prohibidas 
    OFFENSIVE_WORDS = settings.OFFENSIVE_WORDS
    
    # Patrones regex para evasiones como "p@l@br@"
    OFFENSIVE_PATTERNS = settings.OFFENSIVE_PATTERNS

    # 3. Manejo del POST (envío de reseña)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para enviar una reseña.')
            return redirect('login')
            
        form = ReviewForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('comment', '').lower()
            
            # Verificación de contenido ofensivo
            offensive_found = False
            
            # Buscar palabras exactas
            if any(bad_word in comment for bad_word in OFFENSIVE_WORDS):
                offensive_found = True
            
            # Buscar patrones de evasión con regex
            if not offensive_found:
                for pattern in OFFENSIVE_PATTERNS:
                    if re.search(pattern, comment, re.IGNORECASE):
                        offensive_found = True
                        break
            
            if offensive_found:
                messages.error(request, 'Tu reseña contiene lenguaje inapropiado y no será publicada.')
                return redirect('municipality_detail', municipality_id=municipality.id)
            
            # Si pasa la validación, guardar
            review = form.save(commit=False)
            review.municipality = municipality
            review.user = request.user
            review.save()
            messages.success(request, '¡Tu reseña ha sido publicada!')
            return redirect('municipality_detail', municipality_id=municipality.id)
    
    else:
        form = ReviewForm()

    # 4. Cálculo de ratings (existente)
    total_reviews = reviews.count()
    rating_distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    
    for review in reviews:
        rating_distribution[review.rating] += 1
    
    if total_reviews > 0:
        for rating in rating_distribution:
            rating_distribution[rating] = round((rating_distribution[rating] / total_reviews) * 100)

    # 5. Renderizar template con todos los datos
    return render(request, 'municipality_detail.html', {
        'municipality': municipality,
        'accommodations': accommodations,
        'restaurants': restaurants,
        'activities': activities,
        'toll': toll,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'reviews': reviews,
        'form': form,
        'total_reviews': total_reviews,
        'rating_distribution': rating_distribution
    })

# Municipality detail by name
def municipality_detail_by_name(request, municipality_name):
    municipality = get_object_or_404(Municipality, name=municipality_name)
    return render(request, 'municipality_detail.html', {'municipality': municipality})

# FR13 Data analysis - Search count
def track_and_redirect(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)

    # Registrar búsqueda en archivo JSON
    file_path = SEARCH_COUNT_PATH
    
    # Leer archivo si existe
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                search_counts = json.load(file)
            except json.JSONDecodeError:
                search_counts = {}
    else:
        search_counts = {}

    # Actualizar el conteo
    name = municipality.name
    search_counts[name] = search_counts.get(name, 0) + 1

    # Guardar archivo
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(search_counts, file, indent=2)

    # Redirigir al detalle
    return redirect('municipality_detail', municipality_id=municipality.id)



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
    
    # Redirect to detail page if only one municipality and adds 1 to the search count for the municipality found
    if municipalities.count() == 1:

        return redirect('municipality_detail', municipality_id=municipalities.first().id)

    # Show list of municipalities if multiple
    return render(request, 'municipality_list.html', {'municipalities': municipalities})

# FR14 Advanced search with filters and redirection if only one result
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

# Home page with FR13 functionality added (data anal)
def home(request):
    municipalities = list(Municipality.objects.all())
    categories = Category.objects.all()
    locations = Municipality.objects.values_list('location', flat=True).distinct()

    # Ruta al archivo JSON
    json_path = SEARCH_COUNT_PATH

    # Cargar los conteos
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            counts = json.load(f)
    else:
        counts = {}

    # Añadir el contador a cada municipio (si no hay, valor 0)
    for m in municipalities:
        m.search_count = counts.get(m.name, 0)

    # Ordenar municipios de menor a mayor
    municipalities.sort(key=lambda x: x.search_count)

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

##########
# User-generated content system (FR08) ##########
def traveler_post_list_and_create(request):
    posts = TravelerPost.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = TravelerPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Validación de contenido ofensivo
            title = form.cleaned_data.get('title', '').lower()
            content = form.cleaned_data.get('content', '').lower()
            
            # Combinar campos a verificar (ajusta según tu modelo)
            text_to_check = f"{title} {content}"
            
            # Verificar palabras prohibidas
            offensive_word_found = any(
                bad_word in text_to_check 
                for bad_word in settings.OFFENSIVE_WORDS
            )
            
            # Verificar patrones de evasión
            offensive_pattern_found = any(
                re.search(pattern, text_to_check, re.IGNORECASE)
                for pattern in settings.OFFENSIVE_PATTERNS
            )
            
            if offensive_word_found or offensive_pattern_found:
                messages.error(request, 'Tu publicación contiene lenguaje inapropiado y no puede ser publicada.')
                return redirect('traveler_post_list')
            
            # Si pasa la validación, guardar
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()
            messages.success(request, '¡Publicación creada exitosamente!')
            return redirect('traveler_post_list')
    else:
        form = TravelerPostForm()

    return render(request, 'from-traveler-to-traveler.html', {
        'posts': posts,
        'form': form
    })

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(TravelerPost, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('traveler_post_list')

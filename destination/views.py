from django.contrib.auth.decorators import login_required
from .models import Municipality, Event, Activity, Restaurant, Accommodation, Category, Toll, TravelerPost,Favorite, Review
from .forms import TravelerPostForm, ReviewForm
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
import json
import os
import re  # for regex validation of word characters

SEARCH_COUNT_PATH = os.path.join('destination/data', 'search_counts.json')

def municipality_name_list(request):
    municipalities = Municipality.objects.all()
    user_favorites = set()
    
    if request.user.is_authenticated:
        
        user_favorites = set(
            request.user.favorites.values_list('municipality_id', flat=True)
        )
    
    return render(request, 'municipality_list.html', {
        'municipalities': municipalities,
        'user_favorites': user_favorites  
    })

# Municipality detail by ID #(FR16) Moderation system  
def municipality_detail(request, municipality_id):
    #
    municipality = get_object_or_404(Municipality, id=municipality_id)
    accommodations = municipality.accommodations.all()
    restaurants = municipality.restaurants.all()
    activities = municipality.activities.all()
    toll = municipality.tolls.all()
    reviews = municipality.reviews.all().order_by('-created_at')
    
    
    OFFENSIVE_WORDS = settings.OFFENSIVE_WORDS
    
    
    OFFENSIVE_PATTERNS = settings.OFFENSIVE_PATTERNS

    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para enviar una reseña.')
            return redirect('login')
            
        form = ReviewForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('comment', '').lower()
            
            
            offensive_found = False
            
            
            if any(bad_word in comment for bad_word in OFFENSIVE_WORDS):
                offensive_found = True
            
            #w regex
            if not offensive_found:
                for pattern in OFFENSIVE_PATTERNS:
                    if re.search(pattern, comment, re.IGNORECASE):
                        offensive_found = True
                        break
            
            if offensive_found:
                messages.error(request, 'Tu reseña contiene lenguaje inapropiado y no será publicada.')
                return redirect('municipality_detail', municipality_id=municipality.id)
            
            
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

    # Rute al archivo JSON
    json_path = SEARCH_COUNT_PATH

   
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            counts = json.load(f)
    else:
        counts = {}

   
    for m in municipalities:
        m.search_count = counts.get(m.name, 0)
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
        results["accommodations"] = [
            {
                "name": a.name,
                "accommodation_type": a.accommodation_type,
                "website": a.website,
                "image": a.image.url if a.image else ""
            }
            for a in Accommodation.objects.filter(municipality__name=municipality)
        ]

    if "activities" in categories:
        results["activities"] = [
            {
                "name": act.name,
                "description": act.description,
                "image": act.image.url if act.image else ""
            }
            for act in Activity.objects.filter(municipality__name=municipality)
        ]

    if "restaurants" in categories:
        results["restaurants"] = [
            {
                "name": r.name,
                "location": r.location,
                "cuisine_type": r.cuisine_type,
                "image": r.image.url if r.image else ""
            }
            for r in Restaurant.objects.filter(municipality__name=municipality)
        ]

    return JsonResponse(results) 

##########
# User-generated content system (FR08) with the censored requeriment 
#(FR16) Moderation system  ##########
def traveler_post_list_and_create(request):
    posts = TravelerPost.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = TravelerPostForm(request.POST, request.FILES)
        if form.is_valid():
            
            title = form.cleaned_data.get('title', '').lower()
            content = form.cleaned_data.get('content', '').lower()
            
            
            text_to_check = f"{title} {content}"
            
            
            offensive_word_found = any(
                bad_word in text_to_check 
                for bad_word in settings.OFFENSIVE_WORDS
            )
            
           
            offensive_pattern_found = any(
                re.search(pattern, text_to_check, re.IGNORECASE)
                for pattern in settings.OFFENSIVE_PATTERNS
            )
            
            if offensive_word_found or offensive_pattern_found:
                messages.error(request, 'Tu publicación contiene lenguaje inapropiado y no puede ser publicada.')
                return redirect('traveler_post_list')
            
            
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

####(FR19) Favorites system
@login_required
def toggle_favorite(request, municipality_id):
    try:
        municipality = Municipality.objects.get(id=municipality_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            municipality=municipality
        )
        
        if not created:
            favorite.delete()
            is_favorite = False
            message = 'Municipio eliminado de favoritos'
        else:
            is_favorite = True
            message = 'Municipio agregado a favoritos'
        
        # Si es una petición AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'is_favorite': is_favorite,
                'message': message
            })
        
        # Si es una petición normal, redirigir
        messages.success(request, message)
        return redirect('municipality_detail', municipality_id=municipality.id)
        
    except Municipality.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Municipio no encontrado'}, status=404)
        messages.error(request, 'Municipio no encontrado')
        return redirect('home')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=500)
        messages.error(request, 'Ocurrió un error al procesar tu solicitud')
        return redirect('home')



@login_required
def delete_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id, user=request.user)
        municipality_id = review.municipality.id
        review.delete()
        messages.success(request, 'Reseña eliminada exitosamente.')
    except Review.DoesNotExist:
        messages.error(request, 'No se pudo encontrar la reseña.')
    except Exception as e:
        messages.error(request, 'Ocurrió un error al eliminar la reseña.')
    
    return redirect('municipality_detail', municipality_id=municipality_id)

@login_required
def add_review(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.municipality = municipality
            review.user = request.user
            review.save()
            messages.success(request, 'Tu reseña ha sido publicada exitosamente.')
            return redirect('municipality_detail', municipality_id=municipality.id)
    else:
        form = ReviewForm()
    
    return render(request, 'municipality_detail.html', {
        'municipality': municipality,
        'form': form
    })

from .models import Municipality, Event
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
    if query:
        municipalities = Municipality.objects.filter(name__icontains=query).values("id", "name")
        return JsonResponse(list(municipalities), safe=False)
    return JsonResponse([], safe=False)

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
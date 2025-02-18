from django.shortcuts import render
from destination.models import Municipality
from django.http import JsonResponse


def search_municipalities(request):
    query = request.GET.get("q", "").strip()
    if query:
        municipalities = Municipality.objects.filter(name__icontains=query).values("id", "name")
        return JsonResponse(list(municipalities), safe=False)
    return JsonResponse([], safe=False)

# Create your views here.

def home(request):
    return render(request, "home/home.html")


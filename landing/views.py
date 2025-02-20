from django.shortcuts import render
from destination.models import Municipality, Event

# Create your views here.

def landing(request):
    municipalities = Municipality.objects.all()
    return render(request, 'landing.html', {'municipalities': municipalities})
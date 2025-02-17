from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Municipality

# Create your views here.
def municipality_list(request):
    municipalities = Municipality.objects.all()
    return render(request, 'municipality_list.html', {'municipalities': municipalities})

def municipality_name_list(request):
    municipalities = Municipality.objects.all()
    return render(request, 'municipalities_name_list.html', {'municipalities': municipalities})

def municipality_detail(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    return render(request, 'municipality_detail.html', {'municipality': municipality})

def municipality_detail_by_name(request, municipality_name):
    municipality = get_object_or_404(Municipality, name=municipality_name)
    return render(request, 'municipality_detail.html', {'municipality': municipality})
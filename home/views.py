from django.shortcuts import render
from destination.views import municipality_list



# Create your views here.

def home(request):
    return render(request, "home/home.html")


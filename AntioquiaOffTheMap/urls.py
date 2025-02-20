"""
URL configuration for AntioquiaOffTheMap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf.urls.static import static
from django.conf import settings
# Import the views
from destination.views import municipality_list, municipality_detail, municipality_detail_by_name, municipality_name_list, event_calendar
from landing.views import landing
from home.views import search_municipalities


urlpatterns = [
    path('', landing, name='landing'),
    path('municipalities/names', municipality_name_list, name='municipality_name_list'),
    path('admin/', admin.site.urls),
    path('municipalities/', municipality_list, name='municipality_list'), #En esta ruta se listan todas las municipalidades
    path('municipalities/<int:municipality_id>/', municipality_detail, name='municipality_detail'), # con este se lista la municipalidad que coincida con el id
    path('municipalities/<str:municipality_name>/', municipality_detail_by_name, name='municipality_detail_by_name'),
    path("search/", search_municipalities, name="search_municipalities"),
    path('municipalities/<int:municipality_id>/events/', event_calendar, name='municipality_events'),

    path("__reload__/", include("django_browser_reload.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

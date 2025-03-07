from . import views
from django.urls import path, include

urlpatterns = [
    path('municipalities/names', views.municipality_name_list, name='municipality_name_list'),
    path('municipalities/<int:municipality_id>/', views.municipality_detail, name='municipality_detail'),
    path('municipalities/<str:municipality_name>/', views.municipality_detail_by_name, name='municipality_detail_by_name'),
    path("search/", views.search_municipalities, name="search_municipalities"),
    path('municipalities/<int:municipality_id>/events/', views.event_calendar, name='municipality_events'),
    path('', views.home, name='home'),
]
from . import views
from django.urls import path
from .views import municipality_detail, search_municipalities, filtered_search_municipalities, experience_search_page, search_experiences, track_and_redirect,toggle_favorite

urlpatterns = [
    path('municipalities/names', views.municipality_name_list, name='municipality_name_list'),
    path('municipalities/<int:municipality_id>/', views.municipality_detail, name='municipality_detail'),
    path('municipalities/<str:municipality_name>/', views.municipality_detail_by_name, name='municipality_detail_by_name'),
    path('search/', views.search_municipalities, name='search_municipalities'),
    path('municipalities/<int:municipality_id>/events/', views.event_calendar, name='municipality_events'),
    path('', views.home, name='home'),
    path('buscar-experiencias/', experience_search_page, name='experience_search_page'),
    path('experience-search/', search_experiences, name='experience-search'),
    path('filtered-search/', views.filtered_search_municipalities, name='filtered_search_municipalities'),
    path('traveler-posts/', views.traveler_post_list_and_create, name='traveler_post_list'),
    path('traveler-posts/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('track/<int:municipality_id>/', views.track_and_redirect, name='track_and_redirect'),
    path('toggle-favorite/<int:municipality_id>/', toggle_favorite, name='toggle_favorite'),
]

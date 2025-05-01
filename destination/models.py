from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Municipality(models.Model):
    LOCATION_CHOICES = [
        ('Valle de Aburrá', 'Valle de Aburrá'),
        ('Oriente Antioqueño', 'Oriente Antioqueño'),
        ('Suroeste Antioqueño', 'Suroeste Antioqueño'),
        ('Occidente Antioqueño', 'Occidente Antioqueño'),
        ('Nordeste Antioqueño', 'Nordeste Antioqueño'),
        ('Norte Antioqueño', 'Norte Antioqueño'),
        ('Magdalena Medio Antioqueño', 'Magdalena Medio Antioqueño'),
        ('Bajo Cauca Antioqueño', 'Bajo Cauca Antioqueño'),
        ('Urabá Antioqueño', 'Urabá Antioqueño'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name="municipalities")  
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)  
    image = models.ImageField(upload_to='destination/municipalities/', null=True, blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    event_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.date})"

  # FR15 Accommodation Guide Model (Located in model.py) 
class Accommodation(models.Model):
    ACCOMMODATION_TYPES = [
        ('hotel', 'Hotel'),
        ('hostel', 'Hostal'),
        ('rural', 'Alojamiento Rural'),
    ]       

    name = models.CharField(max_length=255)
    accommodation_type = models.CharField(max_length=10, choices=ACCOMMODATION_TYPES)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='accommodations')
    address = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price_range = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='restaurants')
    image = models.ImageField(upload_to='restaurants/', null=True, blank=True) 
    
class Activity(models.Model):
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='activities/', null=True, blank=True)

  
    def __str__(self):
        return f"{self.name} - {self.municipality.name}"

class Toll(models.Model):
    description = models.TextField()
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='tolls')


 

TRAVELER_CATEGORY_CHOICES = [
    ("movilidad", "Movilidad"),
    ("experiencia", "Experiencia en un municipio"),
    ("presupuesto", "Presupuesto de viaje"),
    ("recomendados", "Recomendados increíbles"),
    ("anecdota", "Anécdota"),
    ("consejo", "Consejo para viajeros"),
    ("otras", "Otras"),
]

class TravelerCategory(models.Model):
    name = models.CharField(max_length=50, choices=TRAVELER_CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()
    # models.py

class TravelerPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='traveler_posts/', blank=True, null=True)
    image2 = models.ImageField(upload_to='traveler_posts/', blank=True, null=True)
    image3 = models.ImageField(upload_to='traveler_posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('TravelerCategory')  # ← Usa el nuevo modelo
    municipality = models.ForeignKey('Municipality', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
class Review(models.Model):
    RATING_CHOICES = [
        (5, '★★★★★'),
        (4, '★★★★'),
        (3, '★★★'),
        (2, '★★'),
        (1, '★'),
    ]
    
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_rating_display()} - {self.municipality.name}"

####(FR19) Favorites system

class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='favorites'  
    )
    municipality = models.ForeignKey('Municipality', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'municipality')
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'

    def __str__(self):
        return f"{self.user.username} likes {self.municipality.name}"

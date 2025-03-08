from django.db import models

# Nueva tabla para las categorías
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Municipality(models.Model):
    LOCATION_CHOICES = [
        ('valle_aburra', 'Valle de Aburrá'),
        ('oriente', 'Oriente Antioqueño'),
        ('suroeste', 'Suroeste Antioqueño'),
        ('occidente', 'Occidente Antioqueño'),
        ('nordeste', 'Nordeste Antioqueño'),
        ('norte', 'Norte Antioqueño'),
        ('magdalena_medio', 'Magdalena Medio Antioqueño'),
        ('bajo_cauca', 'Bajo Cauca Antioqueño'),
        ('uraba', 'Urabá Antioqueño'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name="municipalities")  # Ahora es un ManyToMany
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)  # Ahora es un campo de elección
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
    
class Activity(models.Model):
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='activities/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.municipality.name}"

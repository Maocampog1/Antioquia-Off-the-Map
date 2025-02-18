from django.db import models

# Create your models here.
class Municipality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='destination/municipalities/', null=True, blank=True)

class Event(models.Model):
    municipality = models.ForeignKey("Municipality", on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    event_type = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name} ({self.date})"

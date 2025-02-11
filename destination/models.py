from django.db import models

# Create your models here.
class Municipality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='destination/municipalities/', null=True, blank=True)


    def __str__(self):
        return self.name

from django.contrib import admin
from .models import Municipality
from .models import Event

# Register your models here.
admin.site.register(Municipality)
admin.site.register(Event)

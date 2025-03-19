from django.contrib import admin
from .models import Municipality
from .models import Event
from .models import Accommodation
from .models import Category
from .models import Restaurant
from .models import Activity 
from .models import Toll

class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    list_filter = ('location', 'categories')
    search_fields = ('name',)
    filter_horizontal = ('categories',)  

admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Accommodation)
admin.site.register(Restaurant)
admin.site.register(Activity)
admin.site.register(Toll)
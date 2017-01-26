from django.contrib import admin
from .models import NewsPost as GeoNew
from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin

admin.site.register(GeoNew, LeafletGeoAdmin)

# Register your models here.

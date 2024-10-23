from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Weather, AlertConfig

admin.site.register(Weather)
admin.site.register(AlertConfig)

from django.db import models
from django.utils import timezone

class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    main_condition = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)


    daily_max_temp = models.FloatField(null=True, blank=True)
    daily_min_temp = models.FloatField(null=True, blank=True)
    daily_max_wind_speed = models.FloatField(null=True, blank=True)
    daily_min_wind_speed = models.FloatField(null=True, blank=True)
    daily_max_humidity = models.FloatField(null=True, blank=True)
    daily_min_humidity = models.FloatField(null=True, blank=True)
    def __str__(self):
        return f"{self.city}: {self.temperature}°C"
    
class AlertConfig(models.Model):
    
    city = models.CharField(max_length=100, unique=True)
    temp_threshold = models.FloatField(default=35)  

    def __str__(self):
        return f"AlertConfig for {self.city}: Threshold {self.temp_threshold}°C"


class DailyWeatherSummary(models.Model):
    
    city = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)  
    avg_temperature = models.FloatField() 
    max_temperature = models.FloatField() 
    min_temperature = models.FloatField()  
    dominant_condition = models.CharField(max_length=100)  

    def __str__(self):
        return f"Daily Weather Summary for {self.city} on {self.date}: Avg Temp {self.avg_temperature}°C"

    class Meta:
        unique_together = ('city', 'date') 

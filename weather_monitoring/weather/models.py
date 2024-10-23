from django.db import models
from django.utils import timezone

class Weather(models.Model):
    """Model to store weather data for a city."""
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    main_condition = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Weather in {self.city} at {self.timestamp}: {self.temperature}°C, {self.main_condition}"


class AlertConfig(models.Model):
    """Model to store alert configurations for cities."""
    city = models.CharField(max_length=100, unique=True)
    temp_threshold = models.FloatField(default=35)  # Default threshold set to 35°C

    def __str__(self):
        return f"AlertConfig for {self.city}: Threshold {self.temp_threshold}°C"


class DailyWeatherSummary(models.Model):
    """Model to store daily weather summary for a city."""
    city = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)  # Store the date for the summary
    avg_temperature = models.FloatField()  # Average temperature for the day
    max_temperature = models.FloatField()  # Maximum temperature for the day
    min_temperature = models.FloatField()  # Minimum temperature for the day
    dominant_condition = models.CharField(max_length=100)  # Most frequent weather condition of the day

    def __str__(self):
        return f"Daily Weather Summary for {self.city} on {self.date}: Avg Temp {self.avg_temperature}°C"

    class Meta:
        unique_together = ('city', 'date')  # Ensure a unique summary per city and date

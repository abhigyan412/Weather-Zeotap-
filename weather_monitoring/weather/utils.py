import requests
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.db.models import Avg, Max, Min, Count
import time
from collections import Counter
from .models import Weather, AlertConfig

API_KEY = '388396445b31998b3bc4bc9d7ba1b17c'  # Replace with your OpenWeatherMap API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']  
DEFAULT_ALERT_THRESHOLD = 35  # Default temperature alert threshold in Celsius
FETCH_INTERVAL = 300  # Fetch weather data every 5 minutes (300 seconds)

def fetch_weather(city):
    """Fetch the current weather data for a given city from OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {city}: {response.status_code} - {response.text}")
        return None

def save_weather_data(city, data):
    """Save fetched weather data into the Weather model."""
    weather = Weather(
        city=city,
        temperature=data['main']['temp'],
        feels_like=data['main']['feels_like'],
        main_condition=data['weather'][0]['main'],
        timestamp=timezone.now()  # Ensure the timestamp is recorded
    )
    weather.save()
    print(f"Saved weather data for {city}: {weather.temperature}°C, {weather.main_condition}")

def get_weather_data():
    """Continuously fetch weather data for configured cities at intervals."""
    while True:
        for city in CITIES:
            data = fetch_weather(city)
            if data:
                save_weather_data(city, data)
        time.sleep(FETCH_INTERVAL)  # Wait for configured interval before fetching data again

def calculate_daily_summary():
    """Calculate daily weather summaries for the current day."""
    today = timezone.now().date()
    daily_data = Weather.objects.filter(timestamp__date=today)
    
    summaries = []  # Store summaries for each city

    for city in daily_data.values_list('city', flat=True).distinct():
        city_weather = daily_data.filter(city=city)
        
        if city_weather.exists():
            summary = city_weather.aggregate(
                avg_temp=Avg('temperature'),
                max_temp=Max('temperature'),
                min_temp=Min('temperature'),
            )
            
            # Get the dominant weather condition
            dominant_condition = city_weather.values('main_condition').annotate(
                count=Count('main_condition')
            ).order_by('-count').first()
            
            dominant_condition_name = dominant_condition['main_condition'] if dominant_condition else 'N/A'
            
            summaries.append({
                'city': city,
                'avg_temp': summary['avg_temp'],
                'max_temp': summary['max_temp'],
                'min_temp': summary['min_temp'],
                'dominant_condition': dominant_condition_name,
                'date': today, 

            })

    return summaries  # Return the summaries for all cities

def check_alerts():
    """Check if the temperature exceeds the threshold for two consecutive updates."""
    alerts = []  # Store alerts
    for city in CITIES:
        last_two_weather = Weather.objects.filter(city=city).order_by('-timestamp')[:2]
        if len(last_two_weather) == 2:
            # Get user-configurable threshold or use the default
            alert_config = AlertConfig.objects.filter(city=city).first()
            threshold = alert_config.temp_threshold if alert_config else DEFAULT_ALERT_THRESHOLD
            
            # Check if the temperature exceeds the threshold for two consecutive updates
            if all(weather.temperature > threshold for weather in last_two_weather):
                alerts.append(f"Alert: Temperature in {last_two_weather[0].city} exceeded {threshold}°C for two consecutive updates!")

    return alerts

def set_alert_threshold(city, threshold):
    """Set custom alert threshold for a city."""
    config, created = AlertConfig.objects.get_or_create(city=city)
    config.temp_threshold = threshold
    config.save()
    print(f"Alert threshold set for {city}: {threshold}°C")

def run_weather_monitoring():
    """Utility function to summarize and check data at regular intervals."""
    while True:
        get_weather_data()  
        daily_summaries = calculate_daily_summary()  # Save daily summaries for further use or logging
        alerts = check_alerts()  
        print(alerts)  # You might want to log this or handle it as needed
        time.sleep(FETCH_INTERVAL)  

import requests
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.db.models import Avg, Max, Min, Count
import time
from collections import Counter
from .models import Weather, AlertConfig

API_KEY = '388396445b31998b3bc4bc9d7ba1b17c'  
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']  
DEFAULT_ALERT_THRESHOLD = 35  
FETCH_INTERVAL = 300  

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
    
    # Get the current weather data
    temperature = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    main_condition = data['weather'][0]['main']
    
    
    current_weather = Weather.objects.filter(city=city).order_by('-timestamp').first()

    
    if current_weather:
        daily_max_temp = max(current_weather.daily_max_temp, temperature) if current_weather.daily_max_temp is not None else temperature
        daily_min_temp = min(current_weather.daily_min_temp, temperature) if current_weather.daily_min_temp is not None else temperature
        daily_max_humidity = max(current_weather.daily_max_humidity, humidity) if current_weather.daily_max_humidity is not None else humidity
        daily_min_humidity = min(current_weather.daily_min_humidity, humidity) if current_weather.daily_min_humidity is not None else humidity
        daily_max_wind_speed = max(current_weather.daily_max_wind_speed, wind_speed) if current_weather.daily_max_wind_speed is not None else wind_speed
        daily_min_wind_speed = min(current_weather.daily_min_wind_speed, wind_speed) if current_weather.daily_min_wind_speed is not None else wind_speed
    else:
        daily_max_temp = temperature
        daily_min_temp = temperature
        daily_max_humidity = humidity
        daily_min_humidity = humidity
        daily_max_wind_speed = wind_speed
        daily_min_wind_speed = wind_speed

    weather = Weather(
        city=city,
        temperature=temperature,
        feels_like=feels_like,
        humidity=humidity,
        wind_speed=wind_speed,
        main_condition=main_condition,
        timestamp=timezone.now(),
        daily_max_temp=daily_max_temp,          # Store updated daily max temperature
        daily_min_temp=daily_min_temp,          # Store updated daily min temperature
        daily_max_humidity=daily_max_humidity,  # Store updated daily max humidity
        daily_min_humidity=daily_min_humidity,  # Store updated daily min humidity
        daily_max_wind_speed=daily_max_wind_speed,  # Store updated daily max wind speed
        daily_min_wind_speed=daily_min_wind_speed   # Store updated daily min wind speed
    )
    
    weather.save()
    print(f"Saved weather data for {city}: {weather.temperature}°C, {weather.main_condition}, "
          f"Humidity: {weather.humidity}%, Wind Speed: {weather.wind_speed} m/s")



def get_weather_data():
    """Continuously fetch weather data for configured cities at intervals."""
    while True:
        for city in CITIES:
            data = fetch_weather(city)
            if data:
                save_weather_data(city, data)
        time.sleep(FETCH_INTERVAL)  

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
                max_temp=Max('daily_max_temp'),
                min_temp=Min('daily_min_temp'),
                avg_humidity=Avg('humidity'),
                avg_wind_speed=Avg('wind_speed'),
                max_wind_speed=Max('daily_max_wind_speed'), 
                min_wind_speed=Min('daily_min_wind_speed'),  
                max_humidity=Max('daily_max_humidity'),     
                min_humidity=Min('daily_min_humidity'),     
            )

            # Calculate average based on max and min temperatures
            if summary['max_temp'] is not None and summary['min_temp'] is not None:
                avg_temp = (summary['max_temp'] + summary['min_temp']) / 2
            else:
                avg_temp = summary['avg_temp']

            # Calculate average wind speed and humidity
            if summary['max_wind_speed'] is not None and summary['min_wind_speed'] is not None:
                avg_wind_speed = (summary['max_wind_speed'] + summary['min_wind_speed']) / 2
            else:
                avg_wind_speed = summary['avg_wind_speed']

            if summary['max_humidity'] is not None and summary['min_humidity'] is not None:
                avg_humidity = (summary['max_humidity'] + summary['min_humidity']) / 2
            else:
                avg_humidity = summary['avg_humidity']

         
            summaries.append({
                'city': city,
                'date': today,
                'avg_temp': avg_temp,
                'max_temp': summary['max_temp'],
                'min_temp': summary['min_temp'],
                'avg_humidity': avg_humidity, 
                'avg_wind_speed': avg_wind_speed,  
                'max_wind_speed': summary['max_wind_speed'],  
                'min_wind_speed': summary['min_wind_speed'],  
                'max_humidity': summary['max_humidity'],      
                'min_humidity': summary['min_humidity'],      
                'dominant_condition': city_weather.values('main_condition').annotate(count=Count('main_condition')).order_by('-count').first()['main_condition'] if city_weather else 'N/A',
            })

    return summaries



def check_alerts():
    
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
    while True:
        get_weather_data()  
        daily_summaries = calculate_daily_summary()  
        alerts = check_alerts()  
        print(alerts) 
        time.sleep(FETCH_INTERVAL)  

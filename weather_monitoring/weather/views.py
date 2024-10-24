from django.shortcuts import render

from .models import Weather
from .utils import calculate_daily_summary, check_alerts
from django.db.models import Max, Avg, Min  

def weather_dashboard(request):
    # Get the latest weather entry for each city
    latest_weather = Weather.objects.values('city').annotate(latest_timestamp=Max('timestamp'))

    all_latest_weather = []
    
    for entry in latest_weather:
        city_latest = Weather.objects.filter(city=entry['city'], timestamp=entry['latest_timestamp']).first()
        if city_latest:  # Ensure the city_latest is not None before appending
            all_latest_weather.append(city_latest)

    daily_summaries = calculate_daily_summary()  # Calculate daily summary
    alerts = check_alerts()  # Check alerts
    
    return render(request, 'weather/weather_dashboard.html', {
        'all_latest_weather': all_latest_weather,  # Pass the latest weather records to the template
        'daily_summaries': daily_summaries,  # Updated to pass the daily summaries
        'alerts': alerts
    })


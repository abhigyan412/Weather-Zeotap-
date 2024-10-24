from django.shortcuts import render

from .models import Weather
from .utils import calculate_daily_summary, check_alerts
from django.db.models import Max, Avg, Min  

def weather_dashboard(request):
    latest_weather = Weather.objects.values('city').annotate(latest_timestamp=Max('timestamp'))

    all_latest_weather = []
    
    for entry in latest_weather:
        city_latest = Weather.objects.filter(city=entry['city'], timestamp=entry['latest_timestamp']).first()
        if city_latest:  
            all_latest_weather.append(city_latest)

    daily_summaries = calculate_daily_summary() 
    alerts = check_alerts() 
    
    return render(request, 'weather/weather_dashboard.html', {
        'all_latest_weather': all_latest_weather,  
        'daily_summaries': daily_summaries, 
        'alerts': alerts
    })


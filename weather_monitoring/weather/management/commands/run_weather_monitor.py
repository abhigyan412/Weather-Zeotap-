from django.core.management.base import BaseCommand
from weather.utils import run_weather_monitoring

class Command(BaseCommand):
    help = 'Run the weather monitoring function'

    def handle(self, *args, **kwargs):
        run_weather_monitoring()

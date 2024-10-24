# Weather Monitoring System

## Overview

This Weather Monitoring System is a Django-based application that fetches real-time weather data for multiple cities using the OpenWeatherMap API. The system stores the weather data in a PostgreSQL database and provides daily weather summaries, historical trends, and alerts based on temperature thresholds.

## Features

- Fetches current weather data for multiple cities at regular intervals.
- Stores weather data in a PostgreSQL database.
- Calculates and displays daily weather summaries, including:
  - Average temperature
  - Maximum and minimum temperatures
  - Average humidity and wind speed
  - Dominant weather conditions
- Triggers alerts when the temperature exceeds user-defined thresholds.
- Supports custom alert configurations for different cities.

## Technologies Used

- **Django**: Web framework for building the application.
- **PostgreSQL**: Database for storing weather data.
- **OpenWeatherMap API**: Source of real-time weather data.

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd weather-monitoring-system
2. **Create a virtual environment:**

   ```bash
   python -m venv venv


3. **Install required packages:**

   ```bash
   pip install -r requirements.txt

4. **Set up the PostgreSQL database:**
  - Create a new PostgreSQL database.
  - Update the DATABASES setting in settings.py with your database configuration.
5. **Apply migrations:**

   ```bash
   python manage.py migrate
6. **Run the application:**

   ```bash
   python manage.py runserver



## Usage
- Access the application at http://127.0.0.1:8000/ in your web browser.
- The application will automatically fetch and store weather data at the specified intervals.
- You can view daily weather summaries and alerts from the dashboard

##  Acknowledgments

- Django - The web framework used.
- PostgreSQL - The database used for storage.
- OpenWeatherMap API - Source of weather data.

## Configuration
- Set your OpenWeatherMap API key in the utils.py file:
- Configure cities in the CITIES list within utils.py.

-Customize the default temperature alert threshold by modifying the DEFAULT_ALERT_THRESHOLD variable

 ```bash
API_KEY = 'your_openweathermap_api_key'









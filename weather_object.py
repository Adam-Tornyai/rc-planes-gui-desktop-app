from dotenv import load_dotenv
import os
import requests
from geopy import Nominatim
import sys
import json

class Weather:
    def __init__(self, city):
        self.city = city
        self.data = None
        self.location = None
        self.get_location_and_api(city)


    # Get latitude, longitude
    def get_location_and_api(self, city):
        try:
            geolocator = Nominatim(user_agent="rcweather")
            self.location = geolocator.geocode(city)
            if not self.location:
                raise ValueError("Invalid City name")
            latitude = self.location.latitude
            longitude = self.location.longitude
        except Exception as e:
            sys.exit(f"Error: {e}")

        load_dotenv()
        API_KEY = os.getenv('API_KEY')
        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&units=metric&exclude=minutely,daily,alerts&appid={API_KEY}'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise error if not 200
            self.data = response.json()
        except requests.exceptions.RequestException as e:
            sys.exit(f"Couldn't get API response: {e}")


    def extract_weather_data(self, weather_entry):
        temperature = f"{weather_entry['temp']:.1f} °C"
        wind_current = f"{weather_entry['wind_speed']:.1f}" #km/h
        wind_direction = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"][round(weather_entry['wind_deg'] / 45) % 8]
        clouds = f"{weather_entry['clouds']} %"
        description = weather_entry['weather'][0]['description']
        icon = weather_entry['weather'][0]['icon']
        return temperature, wind_current, wind_direction, clouds, description, icon
    
    
    def get_weather_current(self):
        if not self.data:
            return "No weather data available."
        return [self.extract_weather_data(self.data['current'])]


    def get_weather_hourly(self, hours):
        if not self.data:
            return "No weather data available."
        return [self.extract_weather_data(hour) for hour in self.data['hourly'][:hours]]


    def get_position(self):
        if not self.location:
            return "Location not available."
        return self.location.raw['name']
    
    
    def create_test_json_data(self):
        file_path = "test_output.json"
        with open(file_path, "w") as file:
            json.dump(self.data, file)
            print(f"{file_path} was created")
            
            
if __name__ == '__main__':
    # Példa használatra
    city = "Budapest"
    weather = Weather(city)
    print(weather.get_weather_current())
    print(weather.get_weather_hourly(9))
    



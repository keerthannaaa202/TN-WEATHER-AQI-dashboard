import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# City we want weather for
CITY = "Chennai"

# OpenWeatherMap current weather API endpoint
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def fetch_weather():
    response = requests.get(URL)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ SUCCESS! Weather data fetched for", CITY)
        print("-" * 40)
        print(f"Temperature: {data['main']['temp']} °C")
        print(f"Feels like: {data['main']['feels_like']} °C")
        print(f"Humidity: {data['main']['humidity']} %")
        print(f"Weather: {data['weather'][0]['description']}")
        print(f"Wind Speed: {data['wind']['speed']} m/s")
    else:
        print("❌ ERROR:", response.status_code)
        print(response.json())

if __name__ == "__main__":
    fetch_weather()
import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Chennai coordinates
LAT = 13.0827
LON = 80.2707

URL = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"

# AQI index meaning (OpenWeatherMap scale: 1-5)
AQI_LABELS = {
    1: "Good",
    2: "Fair",
    3: "Moderate",
    4: "Poor",
    5: "Very Poor"
}

def fetch_aqi():
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        aqi_index = data['list'][0]['main']['aqi']
        components = data['list'][0]['components']

        print("SUCCESS! AQI data fetched for Chennai")
        print("-" * 40)
        print(f"AQI Index: {aqi_index} ({AQI_LABELS[aqi_index]})")
        print(f"PM2.5: {components['pm2_5']} μg/m3")
        print(f"PM10: {components['pm10']} μg/m3")
        print(f"CO: {components['co']} μg/m3")
        print(f"NO2: {components['no2']} μg/m3")
        print(f"O3: {components['o3']} μg/m3")
    else:
        print("ERROR:", response.status_code)
        print(response.json())

if __name__ == "__main__":
    fetch_aqi()
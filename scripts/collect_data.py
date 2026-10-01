import requests
import os
import csv
from datetime import datetime
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# City config: name + coordinates
CITIES = {
    "Chennai": (13.0827, 80.2707),
    "Coimbatore": (11.0168, 76.9558),
    "Madurai": (9.9252, 78.1198),
    "Salem": (11.6643, 78.1460),
    "Trichy": (10.7905, 78.7047),
    "Tirunelveli": (8.7139, 77.7567),
}

AQI_LABELS = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}

CSV_FILE = "data/weather_aqi_history.csv"

# CSV column headers
HEADERS = [
    "timestamp", "city", "temperature", "feels_like", "humidity",
    "weather_desc", "wind_speed", "aqi_index", "aqi_label",
    "pm2_5", "pm10", "co", "no2", "o3"
]


def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Weather ERROR for {city}: {response.status_code}")
        return None


def fetch_aqi(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"AQI ERROR: {response.status_code}")
        return None


def ensure_csv_exists():
    file_exists = os.path.isfile(CSV_FILE)
    if not file_exists:
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)


def collect_data():
    ensure_csv_exists()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows_added = 0
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        for city, (lat, lon) in CITIES.items():
            weather_data = fetch_weather(city)
            aqi_data = fetch_aqi(lat, lon)

            if weather_data and aqi_data:
                temp = weather_data['main']['temp']
                feels_like = weather_data['main']['feels_like']
                humidity = weather_data['main']['humidity']
                weather_desc = weather_data['weather'][0]['description']
                wind_speed = weather_data['wind']['speed']

                aqi_index = aqi_data['list'][0]['main']['aqi']
                aqi_label = AQI_LABELS[aqi_index]
                components = aqi_data['list'][0]['components']

                writer.writerow([
                    timestamp, city, temp, feels_like, humidity,
                    weather_desc, wind_speed, aqi_index, aqi_label,
                    components['pm2_5'], components['pm10'],
                    components['co'], components['no2'], components['o3']
                ])
                print(f"Saved: {city} | {temp}C | AQI: {aqi_label}")
                rows_added += 1

    print("-" * 40)
    print(f"Done! {rows_added} rows added to {CSV_FILE}")


if __name__ == "__main__":
    collect_data()
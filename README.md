# TN Weather and AQI Real-Time Analytics Dashboard

A real-time data analytics project that collects live weather and air quality (AQI) data for major Tamil Nadu cities, stores it as historical data, predicts short-term trends using machine learning, and visualizes everything on an interactive dashboard.

## Overview

This project automatically fetches live weather and air quality data every 15-30 minutes using the OpenWeatherMap API, builds a growing historical dataset, applies a simple Linear Regression model to forecast upcoming temperature and AQI trends, and displays everything through an interactive Streamlit dashboard with auto-refresh.

## Cities Covered

Chennai, Coimbatore, Madurai, Salem, Trichy, Tirunelveli

## Features

- Live data collection - Real-time weather (temperature, humidity, wind) and air quality (AQI, PM2.5, PM10, CO, NO2, O3) via OpenWeatherMap API
- Automated pipeline - Scheduled data collection using Windows Task Scheduler, no manual intervention needed
- Historical data storage - CSV-based data store that grows over time
- Trend prediction - Linear Regression model forecasts temperature and AQI for the next 1, 3, 6, and 24 hours per city
- Interactive dashboard - Built with Streamlit and Plotly: live metric cards, trend charts, AQI comparisons, and a raw data explorer
- Auto-refresh - Dashboard refreshes automatically every 60 seconds

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| Data Collection | Requests, OpenWeatherMap API |
| Data Processing | Pandas |
| Machine Learning | Scikit-learn (Linear Regression) |
| Visualization | Streamlit, Plotly |
| Scheduling | Windows Task Scheduler |
| Storage | CSV |

## Project Structure

weather-aqi-dashboard/
- data/
  - weather_aqi_history.csv (Historical data, auto-growing)
  - predictions.csv (Latest ML predictions)
- scripts/
  - fetch_weather.py (Test script - weather API)
  - fetch_aqi.py (Test script - AQI API)
  - collect_data.py (Main data collection script)
  - predict.py (ML prediction script)
- dashboard.py (Streamlit dashboard)
- run_collector.bat (Batch file for Task Scheduler)
- .gitignore
- README.md

## Setup and Usage

1. Clone the repository

git clone https://github.com/keerthannaaa202/TN-WEATHER-AQI-dashboard.git
cd TN-WEATHER-AQI-dashboard

2. Install dependencies

pip install requests pandas python-dotenv streamlit plotly scikit-learn streamlit-autorefresh

3. Set up your API key

Get a free API key from OpenWeatherMap (openweathermap.org/api) and create a .env file in the project root:

OPENWEATHER_API_KEY=your_api_key_here

4. Collect data

python scripts/collect_data.py

5. Generate predictions

python scripts/predict.py

6. Run the dashboard

python -m streamlit run dashboard.py

## Future Improvements

- Deploy on Streamlit Cloud for public access
- Add more cities across Tamil Nadu
- Use more advanced forecasting models (ARIMA / Prophet) as historical data grows
- Add email/SMS alerts for poor AQI days
- Migrate from CSV to a proper database (PostgreSQL/SQLite)

## Author

Keerthana A

---
Built as a real-time Data Analytics portfolio project.

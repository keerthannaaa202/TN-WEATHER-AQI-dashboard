@echo off
cd /d C:\Users\keerthana.A\weather-aqi-dashboard
python scripts\collect_data.py >> data\collector_log.txt 2>&1
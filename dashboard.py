import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="TN Weather & AQI Dashboard", layout="wide")

st.title("🌤️ Tamil Nadu Weather & AQI Dashboard")
# Auto-refresh every 60 seconds
st_autorefresh(interval=60 * 1000, key="data_refresh")
st.caption("Live data from OpenWeatherMap — Chennai, Coimbatore, Madurai")

# Load data
@st.cache_data(ttl=60)  # refresh cache every 60 seconds
def load_data():
    df = pd.read_csv("data/weather_aqi_history.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
cities = st.sidebar.multiselect(
    "Select Cities",
    options=df["city"].unique(),
    default=df["city"].unique()
)

filtered_df = df[df["city"].isin(cities)]

# Latest snapshot (most recent timestamp per city)
latest = filtered_df.sort_values("timestamp").groupby("city").tail(1)

st.subheader("📍 Current Snapshot")
cols = st.columns(len(latest))
for idx, (_, row) in enumerate(latest.iterrows()):
    with cols[idx]:
        st.metric(
            label=row["city"],
            value=f"{row['temperature']} °C",
            delta=row["weather_desc"]
        )
        st.caption(f"AQI: {row['aqi_label']} | Humidity: {row['humidity']}%")

st.divider()

# Temperature trend chart
st.subheader("🌡️ Temperature Trend")
fig_temp = px.line(
    filtered_df, x="timestamp", y="temperature", color="city",
    markers=True, title="Temperature Over Time"
)
st.plotly_chart(fig_temp, use_container_width=True)

# AQI trend chart
st.subheader("🌫️ AQI Index Trend")
fig_aqi = px.line(
    filtered_df, x="timestamp", y="aqi_index", color="city",
    markers=True, title="AQI Index Over Time (1=Good, 5=Very Poor)"
)
st.plotly_chart(fig_aqi, use_container_width=True)

# PM2.5 comparison
st.subheader("💨 PM2.5 Levels")
fig_pm25 = px.bar(
    latest, x="city", y="pm2_5", color="city",
    title="Latest PM2.5 by City"
)
st.plotly_chart(fig_pm25, use_container_width=True)

# Raw data table
st.subheader("📋 Raw Data")
st.dataframe(filtered_df.sort_values("timestamp", ascending=False), use_container_width=True)

# Predictions section
st.divider()
st.subheader("Predictions (Linear Trend)")

import os
if os.path.isfile("data/predictions.csv"):
    pred_df = pd.read_csv("data/predictions.csv")
    pred_df["predicted_time"] = pd.to_datetime(pred_df["predicted_time"])
    pred_df_filtered = pred_df[pred_df["city"].isin(cities)]

    if not pred_df_filtered.empty:
        fig_pred_temp = px.line(
            pred_df_filtered, x="hours_ahead", y="predicted_temperature", color="city",
            markers=True, title="Predicted Temperature (next hours)"
        )
        st.plotly_chart(fig_pred_temp, use_container_width=True)

        st.dataframe(pred_df_filtered, use_container_width=True)
    else:
        st.info("No predictions available yet for selected cities. Run scripts/predict.py after more data is collected.")
else:
    st.info("Run python scripts/predict.py first to generate predictions.")
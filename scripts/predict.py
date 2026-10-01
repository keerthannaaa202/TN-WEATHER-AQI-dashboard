import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta

DATA_FILE = "data/weather_aqi_history.csv"
OUTPUT_FILE = "data/predictions.csv"

def load_data():
    df = pd.read_csv(DATA_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def predict_for_city(city_df, target_col, hours_ahead=[1, 3, 6, 24]):
    """Fit a simple linear regression: time -> target_col, predict future values."""
    city_df = city_df.sort_values("timestamp").copy()

    if len(city_df) < 2:
        return None  # not enough data to fit a line

    # Convert timestamp to a numeric feature (hours since first record)
    t0 = city_df["timestamp"].min()
    city_df["hours_elapsed"] = (city_df["timestamp"] - t0).dt.total_seconds() / 3600

    X = city_df[["hours_elapsed"]].values
    y = city_df[target_col].values

    model = LinearRegression()
    model.fit(X, y)

    last_time = city_df["timestamp"].max()
    last_hours_elapsed = city_df["hours_elapsed"].max()

    results = []
    for h in hours_ahead:
        future_hours_elapsed = last_hours_elapsed + h
        pred_value = model.predict([[future_hours_elapsed]])[0]
        future_time = last_time + timedelta(hours=h)
        results.append({
            "predicted_time": future_time,
            "hours_ahead": h,
            "predicted_value": round(pred_value, 2)
        })

    return results


def run_predictions():
    df = load_data()
    cities = df["city"].unique()

    all_predictions = []

    for city in cities:
        city_df = df[df["city"] == city]

        print(f"\n--- {city} ---")

        temp_preds = predict_for_city(city_df, "temperature")
        aqi_preds = predict_for_city(city_df, "aqi_index")

        if temp_preds is None or aqi_preds is None:
            print(f"Not enough data points yet for {city} (need at least 2). Skipping.")
            continue

        for t_pred, a_pred in zip(temp_preds, aqi_preds):
            print(f"In {t_pred['hours_ahead']}h -> Temp: {t_pred['predicted_value']} C | AQI index: {a_pred['predicted_value']}")
            all_predictions.append({
                "city": city,
                "predicted_time": t_pred["predicted_time"],
                "hours_ahead": t_pred["hours_ahead"],
                "predicted_temperature": t_pred["predicted_value"],
                "predicted_aqi_index": a_pred["predicted_value"]
            })

    if all_predictions:
        pred_df = pd.DataFrame(all_predictions)
        pred_df.to_csv(OUTPUT_FILE, index=False)
        print(f"\nPredictions saved to {OUTPUT_FILE}")
    else:
        print("\nNo predictions generated — need more data. Let the collector run longer and try again.")


if __name__ == "__main__":
    run_predictions()
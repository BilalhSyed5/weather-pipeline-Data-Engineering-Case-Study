from typing import List, Dict, Any
import requests
import duckdb
from datetime import datetime

# To get an api key go to https://developer.accuweather.com/ and input it between the "" on the line below
API_KEY = "HqibDSIA6ujO8JADWPvEy6WqnQrt5kCX"
BASE_URL = "http://dataservice.accuweather.com"
CITIES = {
    "Dallas": "351194",
    "Houston": "351197",
    "Austin": "351193"
}

def fetch_weather_data(location_id: str) -> Dict[str, Any]:
    current_conditions_url = f"{BASE_URL}/currentconditions/v1/{location_id}?apikey={API_KEY}"
    forecast_url = f"{BASE_URL}/forecasts/v1/daily/1day/{location_id}?apikey={API_KEY}"
    
    current_response = requests.get(current_conditions_url)
    current_response.raise_for_status()
    forecast_response = requests.get(forecast_url)
    forecast_response.raise_for_status()
    
    current_data = current_response.json()[0]
    forecast_data = forecast_response.json()
    
    return {
        "current": current_data,
        "forecast": forecast_data
    }

def process_weather_data(city: str, data: Dict[str, Any]) -> Dict[str, Any]:
    current = data["current"]
    forecast = data["forecast"]["DailyForecasts"][0]
    
    return {
        "city": city,
        "timestamp": datetime.now().isoformat(),
        "current_temperature": current["Temperature"]["Imperial"]["Value"],
        "current_weather_text": current["WeatherText"],
        "forecast_min_temperature": forecast["Temperature"]["Minimum"]["Value"],
        "forecast_max_temperature": forecast["Temperature"]["Maximum"]["Value"],
        "forecast_day_phrase": forecast["Day"]["IconPhrase"],
        "forecast_night_phrase": forecast["Night"]["IconPhrase"]
    }

def store_data(data: List[Dict[str, Any]]) -> None:
    conn = duckdb.connect("weather_data.db")
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            city VARCHAR,
            timestamp TIMESTAMP,
            current_temperature FLOAT,
            current_weather_text VARCHAR,
            forecast_min_temperature FLOAT,
            forecast_max_temperature FLOAT,
            forecast_day_phrase VARCHAR,
            forecast_night_phrase VARCHAR
        )
    """)
    
    conn.executemany("""
        INSERT INTO weather_data VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, [(
        d["city"],
        d["timestamp"],
        d["current_temperature"],
        d["current_weather_text"],
        d["forecast_min_temperature"],
        d["forecast_max_temperature"],
        d["forecast_day_phrase"],
        d["forecast_night_phrase"]
    ) for d in data])
    
    conn.close()

def main() -> None:
    weather_data = []
    for city, location_id in CITIES.items():
        try:
            raw_data = fetch_weather_data(location_id)
            processed_data = process_weather_data(city, raw_data)
            weather_data.append(processed_data)
        except requests.RequestException as e:
            print(f"Error fetching data for {city}: {e}")
    
    if weather_data:
        store_data(weather_data)
        print("Data fetched and stored successfully.")
    else:
        print("No data was fetched. Please check your API key and internet connection.")

if __name__ == "__main__":
    main()
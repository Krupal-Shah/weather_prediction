import pandas as pd
import requests
import json

def collect_data() -> pd.DataFrame:
    # response = requests.get('https://api.weather.gov/gridpoints/MLB/25,69/forecast') # US
    data = pd.DataFrame()
    offset = 0
    while True:
        response = requests.get(f'https://data.edmonton.ca/resource/s4ws-tdws.json?$offset={offset}')
        new_data = pd.DataFrame(json.loads(response.text))
        if len(new_data) == 0:
            break
        data = pd.concat([data, new_data])
        offset += len(new_data)
    return data

def preprocessing(data) -> pd.DataFrame:
    cols_retain = ["date", "station_id", "station_name", "location", "maximum_temperature_c", "minimum_temperature_c", 'total_rain_mm', 'total_snow_cm', 'total_precipitation_mm', 'snow_on_ground_cm', 'speed_of_maximum_wind_gust_km_h']
    data = data[cols_retain].copy()
    data = data.rename(columns={'station_id': 'id', 'station_name': 'name', 'maximum_temperature_c': 'max_temp', 'minimum_temperature_c': 'min_temp', 'total_rain_mm': 'rain', 'total_snow_cm': 'snow', 'total_precipitation_mm': 'precip', 'snow_on_ground_cm': 'snow_ground', 'speed_of_maximum_wind_gust_km_h': 'wind_speed'})
    data["date"] = pd.to_datetime(data["date"])
    data.set_index("date", inplace=True)
    data.sort_index(inplace=True)
    cols_fill = ['max_temp', 'min_temp', 'snow_ground']
    data[cols_fill] = data[cols_fill].ffill().bfill()
    data.fillna(0, inplace=True)
    return data

def main():
    print("Collecting data...")
    data = collect_data()
    print("Data collected successfully.")
    data = preprocessing(data)
    print("Data preprocessed successfully.")
    data.to_csv("weather_data.csv")
    print('Data stored successfully.')
    return 1

main()


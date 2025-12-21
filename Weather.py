import requests
from datetime import datetime

def get_weather_dataset(api_key, city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    data = requests.get(url).json()

    rain_forecast = 0
    weather = 0
    avg_temp = 0
    avg_humidity = 0

    # only next 6 hours (2 entries)
    item1 = data["list"][0]
    item2 = data["list"][1]

    items = [item1, item2]

    for item in items:
        climate = item["weather"][0]["description"].lower()

        if "rain" in climate:
            rain_forecast = 1
            weather = 2
        elif "cloud" in climate:
            weather = max(weather, 1)

        avg_temp += item["main"]["temp"]
        avg_humidity += item["main"]["humidity"]

    avg_temp = round(avg_temp / 2)
    avg_humidity = round(avg_humidity / 2)


    hour = datetime.strptime(item1["dt_txt"], "%Y-%m-%d %H:%M:%S").hour
    if 0 <= hour < 6:
        time_of_day = 0
    elif 6 <= hour < 12:
        time_of_day = 1
    elif 12 <= hour < 18:
        time_of_day = 2
    else:
        time_of_day = 3

    return {
        "weather": weather,              
        "humidity": avg_humidity,
        "temperature": avg_temp,
        "rain_forecast": rain_forecast,  
        "time_of_day": time_of_day
    }


API_KEY = ""
CITY = "Chennai"
dataset = get_weather_dataset(API_KEY, CITY)
print(dataset)

import requests
from datetime import datetime

def get_weather_data():
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    

    if data.get("cod") != "200":
        return {"error": "API error or city not found"}

    rain_forecast = 0
    weather = 0          # 0=Sunny, 1=Cloudy, 2=Rainy
    avg_temp = 0
    avg_humidity = 0

    # only next 6 hours (2 × 3-hour entries)
    items = data["list"][:2]

    for item in items:
        climate = item["weather"][0]["description"].lower()

        if any(x in climate for x in ["rain", "drizzle", "thunderstorm", "snow"]):
            rain_forecast = 1
            weather = 2
        elif any(x in climate for x in ["cloud", "mist", "fog", "haze", "smoke"]):
            weather = max(weather, 1)

        avg_temp += item["main"]["temp"]
        avg_humidity += item["main"]["humidity"]

    avg_temp = round(avg_temp / len(items))
    avg_humidity = round(avg_humidity / len(items))

    # time of day from first forecast slot
    hour = datetime.strptime(items[0]["dt_txt"], "%Y-%m-%d %H:%M:%S").hour

    if 0 <= hour < 6:
        time_of_day = 0   # Night
    elif 6 <= hour < 12:
        time_of_day = 1   # Morning
    elif 12 <= hour < 18:
        time_of_day = 2   # Afternoon
    else:
        time_of_day = 3   # Evening

    return {
        "weather": weather,            # 0 Sunny | 1 Cloudy | 2 Rainy
        "humidity": avg_humidity,
        "temperature": avg_temp,
        "rain_forecast": rain_forecast,
        "time_of_day": time_of_day,
        "climate":climate
    }
with open("configurations.txt","r") as file:
    for line in file:
        if line.startswith("API_KEY="):
            API_KEY=line.split("=",1)[1].strip().strip('" "')
        if line.startswith("City="):
            CITY=line.split("=",1)[1].strip().strip('" "')









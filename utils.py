import os
import requests

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str) -> str:
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",  # Celsius
        "lang": "pt"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"O clima em {city} está '{description}' com temperatura de {temp}°C."
    else:
        return "Não consegui obter o clima para essa cidade."

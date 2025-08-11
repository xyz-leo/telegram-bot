import os
import requests

# --- API keys ---
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")


def get_help():
    help_text = (
        "Available commands:\n\n"
        "• /start - Start the bot and show this help message\n\n"
        "• /weather <city> - Get current weather for a city\n\n"
        "• /news <topic> - Get the current news for a topic or category\n\n"
        "• /help - Show this help message\n"
        #... add more commands as needed
    )
    return help_text


def get_weather(city: str) -> str:
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",  # Celsius
        "lang": "en",  # English language for weather description"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city} is '{description}' with temperature of {temp}°C."
    else:
        return f"Could not obtain the weather for the specified city. '{city}'"


def get_news(category=None, query=None):
    if query:  # if query exists, use the 'everything' endpoint
        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": NEWSAPI_KEY,
            "q": query,
            "language": "en",
            "pageSize": 10
        }
    else:  # else, find by category in top-headlines
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": NEWSAPI_KEY,
            "category": category or "general",
            "language": "en",
            "country": "us",
            "pageSize": 10
        }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            return "No news found for this topic."
        messages = []
        for art in articles:
            title = art.get("title")
            url = art.get("url")
            messages.append(f"• {title}\nRead more: {url}")
        return "\n\n".join(messages)
    else:
        return "Failed to fetch news."

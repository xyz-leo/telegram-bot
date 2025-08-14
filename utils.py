import requests # for making HTTP requests
from config import OPENWEATHER_API_KEY, NEWSAPI_KEY # for accessing API keys
import json
import os
from reminder import schedule_message_job
from messages import bot_send_message


# --- Get if the message came from an update or query ---
async def get_target_message(update, context):
    if update.message:  # Normal message
        return update.message
    elif update.callback_query:  # Inline button
        await update.callback_query.answer()  # Answer the callback
        return update.callback_query.message
    return None


def get_weather(city: str, lang: str) -> str:
    try:
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",  # Celsius
            "lang": lang,  # English language for weather description"
        }
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return bot_send_message(lang, "weather").format(city=city, description=description, temp=temp)
        else:
            return bot_send_message(lang, "weather_error").format(city=city)         
    except requests.RequestException as e:
        return f"Error connecting to weather service: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


def get_news(category=None, query=None):
    try:
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
    
        response = requests.get(url, params=params, timeout=10)
        
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
    
    except requests.RequestException as e:
        return f"Error connecting to weather service: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


REMINDERS_FILE = "reminders.json"

def load_schedules():
    # Load all scheduled reminders from the JSON file.
    # Returns a dict mapping chat_id (as string) to list of schedules.
    if not os.path.exists(REMINDERS_FILE):
        return {}
    with open(REMINDERS_FILE, "r") as f:
        return json.load(f)


def save_schedules(data):
    # Save all scheduled reminders to the JSON file.
    # 'data' is the full dict of all schedules per chat_id.
    with open(REMINDERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_schedule(chat_id, schedule):
    # Add a new schedule for a specific chat_id.
    # Loads current schedules, appends the new one, then saves back.
    data = load_schedules()
    user_schedules = data.get(str(chat_id), [])
    user_schedules.append(schedule)
    data[str(chat_id)] = user_schedules
    save_schedules(data)


def remove_schedule(chat_id, schedule_id):
    # Remove a schedule by its unique schedule_id for a specific chat_id.
    # Loads schedules, filters out the one to remove, then saves back.
    data = load_schedules()
    user_schedules = data.get(str(chat_id), [])
    user_schedules = [s for s in user_schedules if s["id"] != schedule_id]
    data[str(chat_id)] = user_schedules
    save_schedules(data)


def load_and_schedule_all(job_queue):
    # Load all saved schedules from file and re-schedule them in the running JobQueue.
    # Called on bot startup to restore scheduled reminders in memory.
    data = load_schedules()  # dict: chat_id -> list of schedules
    for chat_id_str, schedules in data.items():
        for sched in schedules:
            time_str = sched["time"]
            job_data = sched
            schedule_message_job(job_queue, int(chat_id_str), time_str, job_data)

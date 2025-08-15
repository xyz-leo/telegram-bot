# user_prefs.py
import json
from pathlib import Path

PREFS_FILE = Path("user_prefs.json")

# Load preferences
try:
    with open(PREFS_FILE, "r", encoding="utf-8") as f:
        USER_PREFS = json.load(f)
except FileNotFoundError:
    USER_PREFS = {}


# --- Function to save preferences ---
def save_user_pref(user_id, key, value):
    """Updates only the necessary key for the user and saves to disk"""
    user_id = str(user_id)
    USER_PREFS[user_id] = USER_PREFS.get(user_id, {})  # Keep existing data
    USER_PREFS[user_id][key] = value
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(USER_PREFS, f, ensure_ascii=False, indent=2)


# --- Language Getters and setters ---
def get_lang(user_id):
    """Return the user's language, default 'pt'."""
    return USER_PREFS.get(str(user_id), {}).get("lang", "pt")

def set_lang(user_id, lang):
    save_user_pref(user_id, "lang", lang)


# --- Bot_calls Getters and setters ---
# --- Bot_calls by type ---
def get_bot_calls(user_id, call_type: str):
    user_data = USER_PREFS.get(str(user_id), {})
    bot_calls = user_data.get("bot_calls", {})
    # guarantee that it is a dict, even if it was int before
    if not isinstance(bot_calls, dict):
        bot_calls = {}
    return bot_calls.get(call_type, 0)


def increment_bot_calls(user_id, call_type: str):
    user_data = USER_PREFS.get(str(user_id), {})
    bot_calls = user_data.get("bot_calls", {})
    if not isinstance(bot_calls, dict):
        bot_calls = {}
    bot_calls[call_type] = bot_calls.get(call_type, 0) + 1
    save_user_pref(user_id, "bot_calls", bot_calls)


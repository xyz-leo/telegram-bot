# user_prefs.py
import json
from pathlib import Path

PREFS_FILE = Path("user_prefs.json")

# Load preferences
if PREFS_FILE.exists():
    with open(PREFS_FILE, "r", encoding="utf-8") as f:
        USER_PREFS = json.load(f)
else:
    USER_PREFS = {}


# --- Get and set user language ---
def get_lang(user_id):
    """Return the user language, or english as default"""
    return USER_PREFS.get(str(user_id), {}).get("lang", "pt")

def set_lang(user_id, lang):
    """Define the user language and saves in disk (user_prefs.json)"""
    USER_PREFS[str(user_id)] = {"lang": lang}
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(USER_PREFS, f, ensure_ascii=False, indent=2)
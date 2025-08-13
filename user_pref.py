# user_prefs.py
import json
from pathlib import Path

PREFS_FILE = Path("user_prefs.json")

# Carregar preferências
if PREFS_FILE.exists():
    with open(PREFS_FILE, "r", encoding="utf-8") as f:
        USER_PREFS = json.load(f)
else:
    USER_PREFS = {}

def get_lang(user_id):
    """Retorna idioma do usuário, ou inglês como padrão."""
    return USER_PREFS.get(str(user_id), {}).get("lang", "en")

def set_lang(user_id, lang):
    """Define idioma do usuário e salva em disco."""
    USER_PREFS[str(user_id)] = {"lang": lang}
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(USER_PREFS, f, ensure_ascii=False, indent=2)
import os

# --- Validation of environment variables ---
def validate_env():
  required_env_vars = ["TELEGRAM_BOT_TOKEN", "OPENWEATHER_API_KEY"]
  for var in required_env_vars:
      if not os.getenv(var):
          raise EnvironmentError(f"Missing environment variable: {var}")

# Run validation
validate_env()


# --- API keys ---

# Telegram bot token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# OpenWeather API key to access weather data
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
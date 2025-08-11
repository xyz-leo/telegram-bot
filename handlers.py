from telegram import Update
from telegram.ext import ContextTypes
from utils import get_weather


# --- Start command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá, Master! O bot está em execução.")


# --- Get the current weather ---
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        city = " ".join(context.args)
        weather_report = get_weather(city)
        await update.message.reply_text(weather_report)
    else:
        city = "São Paulo"
        weather_report = get_weather(city)
        await update.message.reply_text("Cidade não fornecida. Usando 'São Paulo' como padrão.")
        await update.message.reply_text(weather_report)

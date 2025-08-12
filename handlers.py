from telegram import Update
from telegram.ext import ContextTypes
from utils import get_weather, get_news, get_help
import scheduler # for scheduling tasks
import re # for regular expressions, using in the schedule handler


#--- Start command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "Welcome! Here's what I can do for you:\n"
    await update.message.reply_text(welcome_text)
    # Calls the helper handler to show avaiable commands
    await help_command(update, context)


# --- Help command ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = get_help()
    await update.message.reply_text(help_text)


# --- Get the current weather ---
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        city = " ".join(context.args)
        weather_report = get_weather(city)
        await update.message.reply_text(weather_report)
    else:
        city = "São Paulo"
        weather_report = get_weather(city)
        await update.message.reply_text("City not provided. Using 'São Paulo' as standard.")
        await update.message.reply_text(weather_report)


# --- Get the news ---
VALID_TOPICS = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        categories_str = ", ".join(VALID_TOPICS)
        await update.message.reply_text(
            f"You can ask for news categories with /news <category> command. Example: /news music\n\nValid categories are:\n{categories_str}.\n\n"
            "You can also ask for specific topics, like 'linux' or 'bitcoin'."
        )
        return

    messages = []
    for arg in context.args:
        topic = arg.lower()
        if topic in VALID_TOPICS:
            news_text = get_news(category=topic)
            messages.append(f"News for *{topic}*:\n{news_text}")
        else:
            news_text = get_news(query=topic)
            messages.append(f"News about *{topic}*:\n{news_text}")

    await update.message.reply_text("\n\n".join(messages))


# --- Schedule tasks ---
async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n"
            "/schedule <HH:MM> <message>\n"
            "or\n"
            "/schedule <HH:MM> /<handler> [handler_param]\n\n"
            "Example:\n"
            "/schedule 12:00 Hello there!\n"
            "/schedule 15:00 /weather São Paulo"
        )
        return

    time_str = context.args[0]

    if not re.match(r"^\d{2}:\d{2}$", time_str):
        await update.message.reply_text("Time format invalid. Use HH:MM 24-hour format.")
        return

    # If the second arg starts with '/', it is a handeler
    if context.args[1].startswith("/"):
        handler_name = context.args[1][1:]  # remove o "/"
        handler_param = " ".join(context.args[2:]) if len(context.args) > 2 else ""
        job_data = {
            "handler": handler_name,
            "param": handler_param
        }
    else:
        # Simple message (without handler)
        job_data = {
            "handler": None,
            "message": " ".join(context.args[1:])
        }

    scheduler.schedule_message_job(context.job_queue, update.effective_chat.id, time_str, job_data)

    await update.message.reply_text(f"Scheduled your task/message at {time_str}.")
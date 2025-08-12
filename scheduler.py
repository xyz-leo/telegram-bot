import datetime
from telegram.ext import ContextTypes

async def scheduled_message(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    data = context.job.data

    handler = data.get("handler")
    if handler == "weather":
        city = data.get("param") or "São Paulo"
        # import the function get_weather if handler is 'weather'
        from utils import get_weather
        text = get_weather(city)
    elif handler == "news":
        topic = data.get("param") or "general"
        # import the function get_news if handler is 'news'
        from utils import get_news
        text = get_news(category=topic)
    elif handler is None:
        # Simple message
        text = data.get("message", "Hello! This is your scheduled reminder.")
    else:
        text = f"Unknown handler '{handler}'. Cannot execute scheduled task."

    await context.bot.send_message(chat_id=chat_id, text=text)


def schedule_message_job(job_queue, chat_id: int, time_str: str, job_data: dict):
    hour, minute = map(int, time_str.split(":"))

    # Adjusts the time to UTC+3
    hour_utc = (hour + 3) % 24

    # Remove previous jobs with this chat_id
    current_jobs = job_queue.get_jobs_by_name(str(chat_id))
    for job in current_jobs:
        job.schedule_removal()

    job_queue.run_daily(
        scheduled_message,
        time=datetime.time(hour=hour_utc, minute=minute),
        days=(0,1,2,3,4,5,6),
        data=job_data,  # Pass the dict with handler, param or message
        name=str(chat_id),
        chat_id=chat_id
    )

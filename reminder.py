import datetime
from telegram.ext import ContextTypes


async def scheduled_message(context: ContextTypes.DEFAULT_TYPE):
    # Extract the chat ID and job data from the context passed by the job queue
    chat_id = context.job.chat_id
    data = context.job.data

    # Check if the scheduled job is a handler type (e.g., weather or news fetch)
    if data.get("type") == "handler":
        # Clean up handler name, remove leading slash if present
        handler_name = data.get("handler", "").lstrip("/")
        param = data.get("param", "")

        # Handle weather requests by importing and calling the utility function
        if handler_name in ("weather", 'wt'):
            from utils import get_weather
            # Use provided parameter as city or default to "São Paulo"
            text = get_weather(param or "São Paulo")

        # Handle news requests similarly, with validation against known topics
        elif handler_name in ('news', 'nw'):
            from utils import get_news
            from handlers import VALID_TOPICS

            # If param matches a valid topic, get news by category, else use as query string
            if param in VALID_TOPICS:
                text = get_news(category=param)
            else:
                text = get_news(query=param)

        # Unknown handler fallback
        else:
            text = f"Unknown handler '{handler_name}'"

        # Send the resulting text message back to the user in the chat
        await context.bot.send_message(chat_id=chat_id, text=text)
    else:
        # If it's a simple message job, send the stored message text or default reminder text
        message = data.get("message", "Hello! This is your scheduled reminder.")
        await context.bot.send_message(chat_id=chat_id, text=message)


def schedule_message_job(job_queue, chat_id: int, time_str: str, job_data: dict):
    hour, minute = map(int, time_str.split(":"))

    # Convert Brasília (UTC-3) to UTC
    hour_utc = (hour + 3) % 24

    # Remove existing jobs with the same ID
    job_name = f"{chat_id}_{job_data.get('id', '')}"
    for job in job_queue.get_jobs_by_name(job_name):
        job.schedule_removal()

    # Schedule daily repetition
    job_queue.run_daily(
        scheduled_message,
        time=datetime.time(hour=hour_utc, minute=minute),
        days=(0,1,2,3,4,5,6),
        data=job_data,
        name=job_name + "_daily",
        chat_id=chat_id
    )

    return job_name

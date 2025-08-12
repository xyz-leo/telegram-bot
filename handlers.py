from telegram import Update
from telegram.ext import ContextTypes
from utils import get_weather, get_news, get_help, add_schedule, remove_schedule, load_schedules
import reminder # for scheduling tasks
import re
import uuid


#--- Start command ---
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "Welcome! Here's what I can do for you:\n"
    await update.message.reply_text(welcome_text)
    # Calls the helper handler to show avaiable commands
    await help_cmd(update, context)


# --- Help command ---
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = get_help()
    await update.message.reply_text(help_text)


# --- Get the current weather ---
async def weather_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # If user provides city name as arguments, fetch weather for that city
    if context.args:
        city = " ".join(context.args)
        weather_report = get_weather(city)
        await update.message.reply_text(weather_report)
    else:
        # Default city if none provided
        city = "São Paulo"
        weather_report = get_weather(city)
        await update.message.reply_text("City not provided. Using 'São Paulo' as standard.")
        await update.message.reply_text(weather_report)


# --- Get the news ---
VALID_TOPICS = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

async def news_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # If no arguments given, explain valid categories and usage
    if not context.args:
        categories_str = ", ".join(VALID_TOPICS)
        await update.message.reply_text(
            f"You can ask for news categories with /news <category> command. Example: /news music\n\n"
            f"Valid categories are:\n{categories_str}.\n\n"
            "You can also ask for specific topics, like 'linux' or 'bitcoin'."
        )
        return

    messages = []
    # Process each argument: if it's a valid category, fetch news by category; otherwise, search by query
    for arg in context.args:
        topic = arg.lower()
        if topic in VALID_TOPICS:
            news_text = get_news(category=topic)
            messages.append(f"News for *{topic}*:\n{news_text}")
        else:
            news_text = get_news(query=topic)
            messages.append(f"News about *{topic}*:\n{news_text}")

    # Reply with all news messages concatenated
    await update.message.reply_text("\n\n".join(messages))


# --- Schedule Reminders  ---
# Command: /schedule <HH:MM> <message> OR /schedule <HH:MM> <handler> <param>
async def reminder_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /reminder command:
    Usage:
      /reminder <HH:MM> <message>
      OR
      /reminder <HH:MM> /handler param...
    """
    # Validate that user sent at least a time and one argument
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n"
            "/reminder <HH:MM> <message>\n"
            "OR\n"
            "/reminder <HH:MM> /handler <param>\n"
            "Example: /reminder 12:00 /weather Sao Paulo"
        )
        return

    time_str = context.args[0]
    # Validate time format with regex: HH:MM 24-hour
    if not re.match(r"^\d{2}:\d{2}$", time_str):
        await update.message.reply_text("Invalid time format. Use HH:MM 24-hour format.")
        return

    # Generate a unique ID for the scheduled reminder job
    schedule_id = str(uuid.uuid4())

    # If second argument is a handler command starting with '/'
    if context.args[1].startswith("/"):
        handler = context.args[1]
        param = " ".join(context.args[2:]) if len(context.args) > 2 else ""
        job_data = {
            "id": schedule_id,
            "type": "handler",
            "handler": handler,
            "param": param
        }
    else:
        # Otherwise treat all remaining args as plain message
        message = " ".join(context.args[1:])
        job_data = {
            "id": schedule_id,
            "type": "message",
            "message": message
        }

    # Schedule the job using the job queue, passing chat ID, time string, and job data
    job_name = reminder.schedule_message_job(
        context.job_queue,
        update.effective_chat.id,
        time_str,
        job_data
    )

    # Save the scheduled reminder persistently to disk for later reloading
    add_schedule(update.effective_chat.id, {
        "id": schedule_id,
        "time": time_str,
        "job_name": job_name,
        **job_data
    })

    await update.message.reply_text(f"Reminder scheduled at {time_str}. Your job ID: {schedule_id}")


async def lsreminders_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    # Load all schedules for this chat/user
    schedules = load_schedules().get(chat_id, [])

    if not schedules:
        await update.message.reply_text("You have no reminders.")
        return

    # Build a message listing all reminders for the user, formatting per type
    msg_lines = ["Your scheduled tasks:"]
    for sched in schedules:
        sched_id = sched.get("id")
        time = sched.get("time")
        if sched.get("type") == "handler":
            handler = sched.get("handler")
            param = sched.get("param", "")
            msg_lines.append(f"- ID: {sched_id}\n  Time: {time}\n  Handler: {handler} {param}")
        else:
            message = sched.get("message")
            msg_lines.append(f"- ID: {sched_id}\n  Time: {time}\n  Message: {message}")

    await update.message.reply_text("\n\n".join(msg_lines))


async def rmreminder_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    if not context.args:
        await update.message.reply_text("Usage: /remove <schedule_id>")
        return

    schedule_id = context.args[0]
    schedules = load_schedules().get(chat_id, [])

    # Verify the schedule ID exists before removing
    if not any(s.get("id") == schedule_id for s in schedules):
        await update.message.reply_text(f"No reminder found with ID {schedule_id}.")
        return

    # Remove schedule from persistent JSON storage
    remove_schedule(chat_id, schedule_id)

    # Remove the scheduled job from the job queue to stop future triggers
    job_name = f"{chat_id}_{schedule_id}_daily"
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    for job in current_jobs:
        job.schedule_removal()

    await update.message.reply_text(f"Reminder with ID {schedule_id} removed.")

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import get_target_message, get_weather, get_news, add_schedule, remove_schedule, load_schedules
import reminder # for scheduling tasks
import re
import uuid
from messages import bot_send_message
from user_pref import get_lang, set_lang


# ====================== Start command ======================
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    user = update.effective_user.first_name
    await update.message.reply_text(bot_send_message(lang, "welcome").format(user=user))
    await kbd_options_cmd(update=update, context=context)


# ====================== Keyboard options ======================
async def kbd_options_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    
    # Create a keyboard with inline buttons
    keyboard = [
        [InlineKeyboardButton("🌤 Weather", callback_data="weather")],
        [InlineKeyboardButton("📰 News", callback_data="news")],
        [InlineKeyboardButton("📅 List Reminders", callback_data="lsreminders")],
        [InlineKeyboardButton("💬 Switch language", callback_data="language")],
        [InlineKeyboardButton("❓ Help", callback_data="help")],
        
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    target = await get_target_message(update, context)
    
    await target.reply_text(bot_send_message(lang, "options_menu"), reply_markup=reply_markup)


async def button_handler(update, context):
    # Handle button presses
    query = update.callback_query
    data = query.data
    lang = get_lang(query.from_user.id)

    # Answer the callback query to remove the loading indicator
    await query.answer()

    # Handle the button press based on the callback data
    if data == "weather":
        await query.message.reply_text(get_weather("São Paulo", lang))
    elif data == "news":
        await query.message.reply_text(get_news("general"))
    elif data == "lsreminders":
        await lsreminders_cmd(update, context)
    elif data == "language":
        await language_cmd(update=update, context=context)
    elif data == "help":
        await help_cmd(update=update, context=context)


# ====================== Help command ======================
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    user = update.effective_user.first_name
    
    target = await get_target_message(update, context)
    
    await target.reply_text(bot_send_message(lang, "help_text").format(user=user))
    await kbd_options_cmd(update=update, context=context)


# ====================== Language change command ======================
async def language_cmd(update, context):
    # Example: /language pt
    if context.args:
        lang = context.args[0].lower()
        set_lang(update.effective_user.id, lang)
        await update.message.reply_text(bot_send_message(lang, "lang_change").format(lang=lang))
    else: # If no arguments are provided, toggle between 'pt' and 'en'
        lang = get_lang(update.effective_user.id)
        if lang == "pt":
            lang = "en"
            set_lang(update.effective_user.id, lang)
        else:
            lang = "pt"
            set_lang(update.effective_user.id, lang)

    target = await get_target_message(update, context)
    
    await target.reply_text(bot_send_message(lang, "lang_change").format(lang=lang))


# ====================== Get the current weather ======================
async def weather_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    # If user provides city name as arguments, fetch weather for that city
    if context.args:
        city = " ".join(context.args)
        weather_report = get_weather(city, lang)
        await update.message.reply_text(weather_report)
    else:
        # Default city if none provided
        city = "São Paulo"
        weather_report = get_weather(city, lang)
        await update.message.reply_text(bot_send_message(lang, "weather_not_city"))
        await update.message.reply_text(weather_report)


# ====================== Get the news ======================
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


# ====================== Schedule Reminders  ======================
# Command: /schedule <HH:MM> <message> OR /schedule <HH:MM> <handler> <param>
async def reminder_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /reminder command:
    Usage:
      /reminder <HH:MM> <message>
      OR
      /reminder <HH:MM> /handler param...
    """
    
    lang = get_lang(update.effective_user.id)
    # Validate that user sent at least a time and one argument
    if len(context.args) < 2:
        await update.message.reply_text(bot_send_message(lang, "reminder_usage"))
        return

    time_str = context.args[0]
    # Validate time format with regex: HH:MM 24-hour
    if not re.match(r"^\d{2}:\d{2}$", time_str):
        await update.message.reply_text(bot_send_message(lang, "reminder_invalid_time"))
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

    await update.message.reply_text(bot_send_message(lang, "reminder_scheduled").format(time=time_str, schedule_id=schedule_id))


async def lsreminders_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    chat_id = str(update.effective_chat.id)
    # Load all schedules for this chat/user
    schedules = load_schedules().get(chat_id, [])

    if not schedules:
        await update.message.reply_text(bot_send_message(lang, "no_reminders"))
        return

    # Build a message listing all reminders for the user, formatting per type
    msg_lines = [bot_send_message(lang, "lsreminders")]
    for sched in schedules:
        sched_id = sched.get("id")
        time = sched.get("time")
        if sched.get("type") == "handler":
            handler = sched.get("handler")
            param = sched.get("param", "")
            msg_lines.append(bot_send_message(lang, "lsreminders_handler").format(sched_id=sched_id, time=time, handler=handler, param=param))
        else:
            message = sched.get("message")    
            msg_lines.append(bot_send_message(lang, "lsreminders_message").format(sched_id=sched_id, time=time, message=message))

    target = await get_target_message(update, context)

    await target.reply_text("\n\n".join(msg_lines))


async def rmreminder_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    chat_id = str(update.effective_chat.id)
    if not context.args:
        await update.message.reply_text(bot_send_message(lang, "rmreminder_usage"))
        return

    schedule_id = context.args[0]
    schedules = load_schedules().get(chat_id, [])

    # Verify the schedule ID exists before removing
    if not any(s.get("id") == schedule_id for s in schedules):
        await update.message.reply_text(bot_send_message(lang, "rmreminder_not_found").format(schedule_id=schedule_id))
        return

    # Remove schedule from persistent JSON storage
    remove_schedule(chat_id, schedule_id)

    # Remove the scheduled job from the job queue to stop future triggers
    job_name = f"{chat_id}_{schedule_id}_daily"
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    for job in current_jobs:
        job.schedule_removal()

    await update.message.reply_text(bot_send_message(lang, "rmreminder_removed"))

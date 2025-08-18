from telegram import Update 
from telegram.ext import ContextTypes
from utils import send_kbd_menu, get_target_message, get_weather, add_schedule, remove_schedule, load_schedules, translate_text, check_cooldown
import reminder # for scheduling tasks
import re # for regular expressions, used to validate time format
import uuid # for generating unique IDs
from messages import bot_send_message # for sending messages in user language
from user_pref import get_lang, increment_bot_calls, set_lang, get_user_pref # for getting and setting user language
import requests
from datetime import datetime, timedelta # for getting the current date and time


# ====================== Start command ======================
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    user = update.effective_user.first_name
    await update.message.reply_text(bot_send_message(lang, "welcome").format(user=user))
    await main_kbd_cmd(update=update, context=context)
    increment_bot_calls(update.effective_user.id, "start")


# ====================== Handlers for keyboard options ======================
# Command: /options
async def main_kbd_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    
    options = [
        (bot_send_message(lang, "option_weather"), "weather"),
        (bot_send_message(lang, "option_list_reminders"), "lsreminders"),
        (bot_send_message(lang, "option_switch_language"), "language"),
        (bot_send_message(lang, "option_curiosity"), "curiosity"),
        (bot_send_message(lang, "option_userdata"), "userdata"),
        (bot_send_message(lang, "option_exchange"), "exchange"),
        (bot_send_message(lang, "option_holidays"), "holidays"),
        (bot_send_message(lang, "option_help"), "help"),
    ]
    await send_kbd_menu(update, context, options, "options_menu")


async def weather_kbd_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)

    if not check_cooldown(user_id, 5):
        target = await get_target_message(update, context)
        await target.reply_text(bot_send_message(lang, "cooldown_message"))
        return
        
    options = [
        ("São Paulo", "weather|Sao Paulo"),
        ("Minas Gerais", "weather|Minas Gerais"),
        ("Rio de Janeiro", "weather|Rio de Janeiro"),
        ("Bahia", "weather|Bahia"),
        ("Paraná", "weather|Paraná"),
        ("Rio Grande do Sul", "weather|Rio Grande do Sul"),
        ("Pernambuco", "weather|Pernambuco"),
        ("Ceará", "weather|Ceará"),
        ("Fortaleza", "weather|Fortaleza"),
        ("Manaus", "weather|Manaus"),
        
    ]
    await send_kbd_menu(update, context, options, "weather_menu")


# Logic to handle button presses by the user
async def button_handler(update, context):
    # User information
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_lang(user_id)
        
    data = query.data

    # If the data starts with "weather|", it means the user selected a city
    if data.startswith("weather|"):
        if not check_cooldown(user_id):
            await query.answer(bot_send_message(lang, "cooldown_message"), show_alert=True)
            return
            
        city = data.split("|")[1]
        await query.message.reply_text(get_weather(city, lang))
        increment_bot_calls(user_id, "weather")
        
    await query.answer()
    # Handle the button press based on the callback data
    if data == "weather":
        await weather_kbd_menu(update, context)
    elif data == "lsreminders":
        await lsreminders_cmd(update, context)
    elif data == "language":
        await language_cmd(update=update, context=context)
    elif data == "curiosity":
        await curiosity_cmd(update=update, context=context)
    elif data == "userdata":
        await display_user_data_cmd(update=update, context=context)
    elif data == "exchange":
        await exchange_rate(update=update, context=context)
    elif data == "holidays":
        await holidays_cmd(update=update, context=context)
    elif data == "help":
        await help_cmd(update=update, context=context)


# ====================== Help command ======================
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    target = await get_target_message(update, context)
    user = update.effective_user.first_name

    if not check_cooldown(user_id, 5):
        await target.reply_text(bot_send_message(lang, "cooldown_message"))
        return
    
    await target.reply_text(bot_send_message(lang, "help_text").format(user=user))
    await main_kbd_cmd(update=update, context=context)
    increment_bot_calls(user_id, "help")

# ====================== Language change command ======================
async def language_cmd(update, context):
    user_id = update.effective_user.id
    
    # Get the target message (update.message or callback_query)
    target = await get_target_message(update, context)
    lang = get_lang(user_id)
    if not lang:
        lang = 'pt'
        set_lang(user_id, lang)

    if not check_cooldown(user_id, 3):
        await target.reply_text(bot_send_message(lang, "cooldown_message"))
        return
    
    # Example: /language pt
    if context.args:
        lang = context.args[0].lower()
        # Validate the language input
        if lang not in ("pt", "en"):
            return await target.reply_text(bot_send_message(lang, "lang_change_error"))
        else:
            set_lang(user_id, lang)
    else: # If no arguments are provided, toggle between 'pt' and 'en'
        if lang == "pt":
            lang = 'en'
            set_lang(user_id, lang)
        else:
            lang = 'pt'
            set_lang(user_id, lang)

    await target.reply_text(bot_send_message(lang, "lang_change").format(lang=lang))
    increment_bot_calls(user_id, "language_change")

# ====================== Get the current weather ======================
async def weather_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    
    if not check_cooldown(user_id, 4):
        target = await get_target_message(update, context)
        await target.reply_text(bot_send_message(lang, "cooldown_message"))
        return
        
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
        increment_bot_calls(user_id, "weather")

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
    
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    
    if not check_cooldown(user_id, 3):
        target = await get_target_message(update, context)
        await target.reply_text(bot_send_message(lang, "cooldown_message"))
        return
         
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
        user_id,
        time_str,
        job_data
    )

    # Save the scheduled reminder persistently to disk for later reloading
    add_schedule(user_id, {
        "id": schedule_id,
        "time": time_str,
        "job_name": job_name,
        **job_data
    })

    await update.message.reply_text(bot_send_message(lang, "reminder_scheduled").format(time=time_str, schedule_id=schedule_id))
    increment_bot_calls(user_id, "add_reminder")


# ====================== List Reminders ======================
async def lsreminders_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)

    if not check_cooldown(user_id, 5):
        target = await get_target_message(update, context)
        await target.reply_text(bot_send_message(lang, "cooldown_message"))
        return
        
    chat_id = str(update.effective_chat.id)
    # Load all schedules for this chat/user
    schedules = load_schedules().get(chat_id, [])

    if not schedules:
        target = await get_target_message(update, context)
        await target.reply_text(bot_send_message(lang, "no_reminders"))
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
    increment_bot_calls(user_id, "list_reminders")


# ====================== Remove Reminders ======================
async def rmreminder_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_id = update.effective_user.id
    lang = get_lang(user_id)

    if not check_cooldown(user_id):
        target = await get_target_message(update, context)
        await target.reply_text(bot_send_message(lang, "cooldown_message"))
        return
        
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
    increment_bot_calls(user_id, "remove_reminder")


# ====================== Fun Fact command ======================
async def curiosity_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    target = await get_target_message(update, context)

    if not check_cooldown(user_id, 5):
        await target.reply_text(bot_send_message(lang, "cooldown_message"))
        return
    
    try:
        # Make the requisition to the API
        url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
        response = requests.get(url)
        data = response.json()

        fact = data.get("text", bot_send_message(lang, "curiosity_error"))
        if lang == "pt":
            fact = translate_text(fact, source="en", target="pt")

        await target.reply_text(bot_send_message(lang, "curiosity_disclaimer"))
        await target.reply_text(bot_send_message(lang, "curiosity_message").format(fact=fact))
        increment_bot_calls(user_id, "curiosity")
    except Exception as e:
        await target.reply_text(bot_send_message(lang, "curiosity_error"))
        


# ====================== Translate ======================
async def translate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    target = await get_target_message(update, context)

    if not check_cooldown(user_id, 5):
        await target.reply_text(bot_send_message(lang, "cooldown_message"))
        return

    # Check if the user provided the necessary arguments
    if len(context.args) < 3:
        languages = [
            "afrikaans", "albanian", "amharic", "arabic", "armenian", "assamese",
            "aymara", "azerbaijani", "bambara", "basque", "belarusian", "bengali",
            "bhojpuri", "bosnian", "bulgarian", "catalan", "cebuano", "chichewa",
            "chinese (simplified)", "chinese (traditional)", "corsican", "croatian",
            "czech", "danish", "dhivehi", "dogri", "dutch", "english", "esperanto",
            "estonian", "ewe", "filipino", "finnish", "french", "frisian", "galician",
            "georgian", "german", "greek", "guarani", "gujarati", "haitian creole",
            "hausa", "hawaiian", "hebrew", "hindi", "hmong", "hungarian", "icelandic",
            "igbo", "ilocano", "indonesian", "irish", "italian", "japanese", "javanese",
            "kannada", "kazakh", "khmer", "kinyarwanda", "konkani", "korean", "krio",
            "kurdish (kurmanji)", "kurdish (sorani)", "kyrgyz", "lao", "latin",
            "latvian", "lingala", "lithuanian", "luganda", "luxembourgish",
            "macedonian", "maithili", "malagasy", "malay", "malayalam", "maltese",
            "maori", "marathi", "meiteilon (manipuri)", "mizo", "mongolian", "myanmar",
            "nepali", "norwegian", "odia (oriya)", "oromo", "pashto", "persian",
            "polish", "portuguese", "punjabi", "quechua", "romanian", "russian",
            "samoan", "sanskrit", "scots gaelic", "sepedi", "serbian", "sesotho",
            "shona", "sindhi", "sinhala", "slovak", "slovenian", "somali", "spanish",
            "sundanese", "swahili", "swedish", "tajik", "tamil", "tatar", "telugu",
            "thai", "tigrinya", "tsonga", "turkish", "turkmen", "twi", "ukrainian",
            "urdu", "uyghur", "uzbek", "vietnamese", "welsh", "xhosa", "yiddish",
            "yoruba", "zulu"
        ]

        # Format the list of languages into a string
        languages = ", ".join([f"{v}" for v in languages])
        return await target.reply_text(bot_send_message(lang, "translate_usage").format(languages=languages))

    source_lang = context.args[0].lower()
    target_lang = context.args[1].lower()
    text_to_translate = " ".join(context.args[2:])

    # Calls the utilitary function
    translated = translate_text(text_to_translate, source=source_lang, target=target_lang)

    await target.reply_text(bot_send_message(lang, "translated_message").format(source=source_lang, target=target_lang, translated=translated))
    increment_bot_calls(user_id, "translate")


# ====================== Display User Data ======================
async def display_user_data_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    lang = get_lang(user_id)
    target = await get_target_message(update, context)
    
    if not check_cooldown(user_id, 3):
        await target.reply_text(bot_send_message(lang, "cooldown_message"))
        return
        
    data =  get_user_pref(user_id)
    commands = ""

    # Iterate over the bot_calls dictionary and format the string
    for command, count in data['bot_calls'].items():
        commands += f"{command}: {count}\n"

    await target.reply_text(bot_send_message(lang, "user_data").format(user_name=user_name, user_id=user_id, lang=lang, commands=commands))
    
    increment_bot_calls(user_id, "request_user_data")


# ====================== From API: https://brasilapi.com.br/ ======================
#  --- Get info for a Brasilian CEP ---
async def br_cep_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)

    if not check_cooldown(user_id, 5):
        await update.message.reply_text(bot_send_message(lang, "cooldown_message"))
        return
    
    if not context.args:
        await update.message.reply_text(bot_send_message(lang, "cep_usage"))
        return
        
    cep = context.args[0]
    if not re.match(r"^\d{5}-?\d{3}$", cep):
        await update.message.reply_text(bot_send_message(lang, "cep_error"))
        return
            
    url = f"https://brasilapi.com.br/api/cep/v1/{cep}"
    try:
        response = requests.get(url, timeout=5)

        data = response.json()

        # Check if the CEP was found
        if "service_error" in data.values():
            await update.message.reply_text(bot_send_message(lang, "cep_not_found").format(cep=cep))
            return
            
        # Format the data to be sent to the user
        msg = "\n".join([f"{str(k.upper())}: {v}" for k, v in data.items()])

        await update.message.reply_text(bot_send_message(lang, "cep_info").format(data=msg))
        
        increment_bot_calls(user_id, "cep_search")
    except Exception as e:
        print(e)


# --- Exchange rate ---
async def exchange_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    target = await get_target_message(update, context)

    # Checks cooldown
    if not check_cooldown(user_id, 5):
        await target.reply_text(bot_send_message(lang, "cooldown_message"))
        return

    # Defaults
    coin = "USD"
    date_str = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Verify arguments provided by the user
    if context.args:
        # Validate coin (3 letters)
        if not re.fullmatch(r"[A-Za-z]{3}", context.args[0]):
            return await target.reply_text(bot_send_message(lang, "coin_usage"))
        coin = context.args[0].upper()

        # Validate optional date
        if len(context.args) > 1 and re.match(r"^\d{4}-\d{2}-\d{2}$", context.args[1]):
            date_str = context.args[1]
        elif len(context.args) > 1:
            return await target.reply_text(bot_send_message(lang, "coin_usage"))

    url = f"https://brasilapi.com.br/api/cambio/v1/cotacao/{coin}/{date_str}"

    try:
        res = requests.get(url)
        data = res.json()

        # Get closing price
        fechamento_ptax = data["cotacoes"][-1]

        # Format message to the user
        msg = "\n".join([f"{str(k).upper()}: {v}" for k, v in fechamento_ptax.items()])

        await target.reply_text(bot_send_message(lang, "coin_info").format(coin=coin, date=date_str, msg=msg))

        increment_bot_calls(user_id, "coin_search")

    except Exception as e:
        print(e)
        await target.reply_text(bot_send_message(lang, "coin_usage").format(coin=coin))


# --- CPNJ Lookup ---
async def cnpj_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)

    if not check_cooldown(user_id, 5):
        await update.message.reply_text(bot_send_message(lang, "cooldown_message"))
        return

    if not context.args:
        await update.message.reply_text(bot_send_message(lang, "cnpj_usage"))
        return

    # Validate CNPJ format
    cnpj = context.args[0]
    if not re.fullmatch(r"\d{14}|(\d{2}\.\d{3}\.\d{3}-\d{4}-\d{2})", cnpj):
        await update.message.reply_text(bot_send_message(lang, "cnpj_invalid"))
        return

    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        # Check if the CNPJ was not found
        if "bad_request" in data.values():
            await update.message.reply_text(bot_send_message(lang, "cnpj_error").format(cnpj=cnpj))
            return
            
        msg = "\n".join([f"{str(k).upper()}: {v}\n" for k, v in data.items()])
        
        await update.message.reply_text(bot_send_message(lang, "cnpj_info").format(data=msg, cnpj=cnpj))
        
        increment_bot_calls(user_id, "cnpj_search")
    except Exception as e:
        print(e)


async def holidays_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    target = await get_target_message(update, context)

    if not check_cooldown(user_id, 5):
        await target.reply_text(bot_send_message(lang, "cooldown_message"))
        return

    if context.args:
        year = context.args[0]
    else:
        year = datetime.now().year
        
    url = f"https://brasilapi.com.br/api/feriados/v1/{year}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        # Format the data to be sent to the user
        msg = ""
        for holiday in data:
            msg += f"Nome: {holiday['name']}\nData: {holiday['date']}\nTipo: {holiday['type']}\n__________________________________\n"
        
        await target.reply_text(msg)
        
    except Exception as e:
        print(e)
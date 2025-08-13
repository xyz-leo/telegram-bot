from telegram.ext import ApplicationBuilder, CommandHandler
import handlers
from config import TOKEN
from utils import load_and_schedule_all


# --- Register handlers ---
def register_handlers(app):
    commands = [
        (["start", "st"], handlers.start_cmd),
        (["help", "hp"], handlers.help_cmd),
        (["language", "lg"], handlers.language_cmd),
        (["weather", "wt"], handlers.weather_cmd),
        (["news", "nw"], handlers.news_cmd),
        (["reminder", "re"], handlers.reminder_cmd),
        (["lsreminders", "lsre"], handlers.lsreminders_cmd),
        (["rmreminder", "rmre"], handlers.rmreminder_cmd),
    ]
    for cmd_list, func in commands:
        for cmd in cmd_list:
            app.add_handler(CommandHandler(cmd, func))

    
# --- Main loop ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    register_handlers(app)
    load_and_schedule_all(app.job_queue)
    app.run_polling()
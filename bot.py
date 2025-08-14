from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
import handlers
from config import TOKEN
from utils import load_and_schedule_all


# --- Register handlers ---
def register_handlers(app):
    commands = [
        (["start", "st"], handlers.start_cmd),
        (["options", "op"], handlers.main_kbd_cmd),
        (["help", "hp"], handlers.help_cmd),
        (["language", "lg"], handlers.language_cmd),
        (["weather", "wt"], handlers.weather_cmd),
        (["reminder", "re"], handlers.reminder_cmd),
        (["lsreminders", "lsre"], handlers.lsreminders_cmd),
        (["rmreminder", "rmre"], handlers.rmreminder_cmd),
    ]
    # Register all commands above
    for cmd_list, func in commands:
        for cmd in cmd_list:
            app.add_handler(CommandHandler(cmd, func))

    # Register the handler function to handle button presses
    app.add_handler(CallbackQueryHandler(handlers.button_handler))


# --- Main loop ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    register_handlers(app)
    load_and_schedule_all(app.job_queue)
    app.run_polling()
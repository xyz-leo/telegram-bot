from telegram.ext import ApplicationBuilder, CommandHandler
import handlers
from config import TOKEN

# --- Register handlers ---
def register_handlers(app):
    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("help", handlers.help_command))
    app.add_handler(CommandHandler("weather", handlers.weather))
    app.add_handler(CommandHandler("news", handlers.news))


# --- Main loop ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    register_handlers(app)
    app.run_polling()

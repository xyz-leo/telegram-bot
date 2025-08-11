from telegram.ext import ApplicationBuilder, CommandHandler
import handlers
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("help", handlers.help_command))
    app.add_handler(CommandHandler("weather", handlers.weather))
    app.add_handler(CommandHandler("news", handlers.news))
    app.run_polling()

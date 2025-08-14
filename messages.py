MESSAGES = {
  "pt": {
      # ====================== Help message ======================
      "help_text": (
          "👋 Olá, {user}!\n"
          "❗ Todos os comandos começam com '/' e também possuem uma abreviação.\n\n"
          "Aqui estão os comandos disponíveis para este bot:\n\n"
          "• ▶️ /st ou /start - Iniciar o chat com o bot.\n\n"
          "• 🤖 /options ou /op - Mostrar menu de opções rápidas.\n\n"
          "• 💬 /lg ou /language <pt|en> - Mudar idioma. Exemplo: /lg pt\n\n"
          "• 🌦️ /wt ou /weather <city> - Checar previsão do tempo em uma cidade. Exemplo: /weather Sao Paulo\n\n"
          "• 📰 /nw ou /news <topic> - Checar as notícias de um tópico ou categoria. Exemplo: /news esportes\n\n"
          "• 📝 /re ou /reminder <HH:MM> <message> - Agendar uma mensagem para ser enviada numa hora específica, todos os dias.\n\n"
          "• 📅 /lsre or /lsreminders - Listar todos os lembretes agendados.\n\n"
          "• 🗑️ /rmre or /rmreminder <schedule_id> - Remove um lembrete agendado pelo ID. você pode pegar o ID com o comando /lsreminders\n\n"
          "• ❓ /hp or /help - Mostra essa mensagem de ajuda.\n"
          #... add more commands as needed
      ),

      
      # ====================== Welcome message ======================
      "welcome": "👋 Olá, seja bem-vindo, {user}!\n\nEu sou seu bot de lembretes, projetado por xyz-leo.\nEu posso te mandar mensagens agendadas para te lembrar de tarefas, eventos, clima ou qualquer coisa importante.\n\nPor favor, digite /help para consultar informações e comandos e disponíveis.",

      
      # ====================== Options menu message ======================
      "options_menu": "😊 O que você deseja fazer?",
      
      
      # ====================== language change message ======================
      "lang_change": "💬 Idioma definido para português brasileiro, {lang}-BR",
      
      
      # ====================== Weather message ======================
      "weather": "🌦️ O clima em {city} está '{description}' com a temperatura de {temp}°C.",
      "weather_not_city": "Cidade não fornecida. Usando 'São Paulo' como padrão.",
      "weather_error": "❗ Não foi possível obter o clima para a cidade especificada. '{city}'",

      
      # ====================== Reminders ======================
      "reminder_usage": "Uso:\n/reminder <HH:MM> <message>\nOU\n/reminder <HH:MM> /handler <param>\nExemplo: /reminder 12:00 /weather Sao Paulo",
      "reminder_invalid_time": "❗ Formato de hora inválido. Use o formato HH:MM 24 horas.",
      "reminder_scheduled": "📝 Lembrete agendado às {time}.",
      
      # List reminders
      "no_reminders": "Você não tem lembretes.",
      "lsreminders": "📅 Aqui estão seus lembretes agendados:",
      "lsreminders_handler": "___________________________________________\n📨 Handler: {handler} {param}\n\n⏰ Hora: {time}\n\n🆔: {sched_id}\n___________________________________________",
      "lsreminders_message": "___________________________________________\n📨 Mensagem: {message}\n\n⏰ Hora: {time}\n\n🆔: {sched_id}\n___________________________________________",

      #  Remove reminders
      "rmreminder_usage": "Uso: /rmreminder <schedule_id>",
      "rmreminder_not_found": "❗ Nenhum lembrete encontrado com o ID {schedule_id}.",
      "rmreminder_removed": "🗑️ Lembrete removido.",
      
      # ====================== Unknown command message ======================
      "unknown": "❓ Não entendi. Digite /help para ver os comandos",
  },
  "en": {
      # ====================== Help message ======================
      "help_text": (
          "\n❗ All commands start with '/' and also have an abbreviation. If you prefeer, you can type /op to show quick commands\n\n"
          "Here is the available commands for this bot:\n\n"
          "• ▶️ /st or /start - Start chatting with the bot\n\n"
          "• 🤖 /options or /op - Show quick options menu.\n\n"
          "• 💬 /lg or /language <pt|en> - Change the language. Example: /lg pt\n\n"
          "• 🌦️ /wt or /weather <city> - Get current weather for a city. Example: /weather Sao Paulo\n\n"
          "• 📰 /nw or /news <topic> - Get the current news for a topic or category. Example: /news sports\n\n"
          "• 📝 /re or /reminder <HH:MM> <message> - Schedule a message to be sent at a specific time, everyday\n\n"
          "• 📅 /lsre or /lsreminders - List all scheduled reminders\n\n"
          "• 🗑️ /rmre or /rmreminder <schedule_id> - Remove a scheduled reminder by ID. You can get the ID with the command /lsreminders\n\n"
          "• ❓ /hp or /help - Show this help message\n"
          #... add more commands as needed
      ),

      
      # ====================== Welcome message ======================
      "welcome": "👋 Hello, welcome, {user}!\n\nI’m your personal reminder bot, projected by xyz-leo.\nI can send you scheduled messages to help you remember tasks, events, weather or anything important.\n\nPlease, type /help to check information and avaiable commands.",

      
      # ====================== Options menu message ======================
      "options_menu": "😊 What do you want to do?",

      
      #  ====================== language change message ======================
      "lang_change": "💬 Language set to American English, {lang}-US",
      
      
      # ====================== Weather ======================
      "weather": "🌦️ The weather in {city} is '{description}' with temperature of {temp}°C.",
      "weather_not_city": "City not provided. Using 'São Paulo' as standard.",
      "weather_error": "❗ Could not obtain the weather for the specified city. '{city}'",


      # ====================== Reminders ======================
      "reminder_usage": "Usage:\n/reminder <HH:MM> <message>\nOR\n/reminder <HH:MM> /handler <param>. Example: /reminder 12:00 /weather Sao Paulo",
      "reminder_invalid_time": "❗ Invalid time format. Use HH:MM 24-hour format.",
      "reminder_scheduled": "📝 Reminder scheduled at {time}.",

      # List reminders
      "no_reminders": "You have no reminders.",
      "lsreminders": "📅 Here are your scheduled reminders:",
      "lsreminders_handler": "___________________________________________\n📨 Handler: {handler} {param}\n\n⏰ Time: {time}\n\n🆔: {sched_id}\n___________________________________________",
      "lsreminders_message": "___________________________________________\n📨 Message: {message}\n\n⏰ Time: {time}\n\n🆔: {sched_id}\n___________________________________________",

      #  Remove reminders
      "rmreminder_usage": "Usage: /rmreminder <schedule_id>",
      "rmreminder_not_found": "❗ No reminder found with ID {schedule_id}.",
      "rmreminder_removed": "🗑️ Reminder removed.",
      
      # ====================== Unknown command message ======================
      "unknown": "❓ I didn’t understand. Type /help to see commands.",
  }
}

# --- Get message in user language ---
def bot_send_message(user_lang, key):
  """Returns message in the user language, or portuguese fallback"""
  return MESSAGES.get(user_lang, MESSAGES["pt"]).get(key, key)
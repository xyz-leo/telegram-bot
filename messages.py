MESSAGES = {
  "pt": {
      # ====================== Help message ======================
      "help_text": (
          "👋 Olá, {user}, precisa de ajuda?\n\n"
          "❗ Todos os comandos começam com '/' e também possuem uma abreviação. Se preferir, digite /op quando precisar listar as opções rápidas.\n\n"
          "Aqui estão os comandos disponíveis para este bot:\n\n"
          "• ▶️ /st ou /start - Iniciar o chat com o bot.\n\n"
          "• 🤖 /op ou /options - Mostrar menu de opções rápidas. Seu melhor amigo.\n\n"
          "• 💬 /lg ou /language <pt|en> - Mudar idioma. Exemplo: /lg pt\n\n"
          "• 🌤 /wt ou /weather <city> - Checar previsão do tempo em uma cidade. Exemplo: /weather Sao Paulo\n\n"
          "• 🦜 /tr ou /translate <de> <para> <text> - Traduzir texto de um idioma para outro. Exemplo: /translate en pt Hello world!\n\n"
          "• 📝 /re ou /reminder <HH:MM> <message> - Agendar uma mensagem para ser enviada numa hora específica, todos os dias.\n\n"
          "• 📅 /lsre or /lsreminders - Listar todos os lembretes agendados.\n\n"
          "• 🗑️ /rmre or /rmreminder <schedule_id> - Remove um lembrete agendado pelo ID. você pode pegar o ID com o comando /lsreminders\n\n"
          "• 💡 /cr ou /curiosity - Envia uma curiosidade aleatória.\n\n"
          "• ❓ /hp or /help - Mostra essa mensagem de ajuda.\n"
          #... add more commands as needed
      ),

      
      # ====================== Welcome message ======================
      "welcome": "👋 Olá, seja bem-vindo, {user}!\n\nEu sou seu bot de lembretes, projetado por xyz-leo.\nEu posso te mandar mensagens agendadas para te lembrar de tarefas, eventos, clima ou qualquer coisa importante.\n\nPor favor, digite /help para consultar informações e comandos e disponíveis.",

      
      # ====================== Options menu message ======================
      # Options
      "option_weather": "🌤 Ver clima",
      "option_list_reminders": "📅 Listar lembretes",
      "option_switch_language": "💬 Mudar idioma",
      "option_help": "❓ Ajuda",
      
      # Menu
      "options_menu": "😊 O que você deseja fazer agora?",
      "weather_menu": "Se o estado/cidade não estiver listado, digite manualmente com /weather <city>. Exemplo: /weather São Paulo\n\n🌤 Qual estado deseja ver o clima?",
      
      
      # ====================== language change message ======================
      "lang_change": "💬 Idioma definido para português brasileiro, {lang}-BR",
      "lang_change_error": "❗ Idioma inválido. Use 'pt' ou 'en'.",
      
      
      # ====================== Weather message ======================
      "weather": "🌤 O clima em {city} está '{description}' com a temperatura de {temp}°C.",
      "weather_not_city": "Cidade não fornecida. Usando 'São Paulo' como padrão.",
      "weather_error": "❗ Não foi possível obter o clima para a cidade especificada. '{city}'",

      
      # ====================== Reminders ======================
      "reminder_usage": "Uso:\n/reminder <HH:MM> <message>\nOU\n/reminder <HH:MM> /handler <param>\nExemplo: /reminder 12:00 /weather Sao Paulo",
      "reminder_invalid_time": "❗ Formato de hora inválido. Use o formato HH:MM 24 horas.",
      "reminder_scheduled": "📝 Lembrete agendado às {time}.",
      
      # List reminders
      "no_reminders": "Você não tem lembretes.",
      "lsreminders": "📅 Aqui estão seus lembretes agendados:\n___________________________________________",
      "lsreminders_handler": "📨 Handler: {handler} {param}\n\n⏰ Hora: {time}\n\n🆔: {sched_id}\n___________________________________________",
      "lsreminders_message": "📨 Mensagem: {message}\n\n⏰ Hora: {time}\n\n🆔: {sched_id}\n___________________________________________",

      #  Remove reminders
      "rmreminder_usage": "Uso: /rmreminder <schedule_id>",
      "rmreminder_not_found": "❗ Nenhum lembrete encontrado com o ID {schedule_id}.",
      "rmreminder_removed": "🗑️ Lembrete removido.",

      
      # ====================== Curiosity ======================
      "curiosity": "💡 Curiosidade",
      "curiosity_message": "💡 Curiosidade:\n\n{fact}",
      "curiosity_disclaimer": "⚠️ A curiosidade pode não ser verdadeira. Este comando é apenas para diversão.",
      "curiosity_error": "❗ Não foi possível obter uma curiosidade agora.",

      
      # ====================== Translate ======================
      "translated_message": "🦜 Traduzido ({source} → {target}):\n\n{translated}",
      "translate_usage": "Uso: /translate <de> <para> <text>\nExemplo: /translate en pt Hello world!",

      
      # ====================== Cooldown message ======================
      "cooldown_message": "⏳ Você está clicando muito rápido. Aguarde alguns segundos antes de tentar novamente.",

      
      # ====================== User Data ======================
      "userdata": "👤 Dados do Usuário",
      "user_data": "👤 Dados do Usuário\n___________________________________________\nNome: {user_name}\nID: {user_id}\nLanguage: {lang}-BR\n\nComandos solicitados:\n{commands}",
      
      
      # ====================== Unknown command message ======================
      "unknown": "❓ Não entendi. Digite /help para ver os comandos",
  },
  "en": {
      # ====================== Help message ======================
      "help_text": (
          "👋 Hello, {user}, need help?\n\n"
          "❗ All commands start with '/' and also have an abbreviation. If you prefeer, you can type /op when you need to list the quick commands!\n\n"
          "Here is the available commands for this bot:\n\n"
          "• ▶️ /st or /start - Start chatting with the bot\n\n"
          "• 🤖 /op or /options - Show quick options menu. Your best friend.\n\n"
          "• 💬 /lg or /language <pt|en> - Change the language. Example: /lg pt\n\n"
          "• 🌤 /wt or /weather <city> - Get current weather for a city. Example: /weather Sao Paulo\n\n"
          "• 🦜 /tr ou /translate <from> <to> <text> - Translate text from one language to another. Example: /translate en pt Hello world!\n\n"
          "• 📝 /re or /reminder <HH:MM> <message> - Schedule a message to be sent at a specific time, everyday\n\n"
          "• 📅 /lsre or /lsreminders - List all scheduled reminders\n\n"
          "• 🗑️ /rmre or /rmreminder <schedule_id> - Remove a scheduled reminder by ID. You can get the ID with the command /lsreminders\n\n"

          "• 💡 /cr ou /curiosity - Send a random curiosity.\n\n"
          "• ❓ /hp or /help - Show this help message\n"
          #... add more commands as needed
      ),

      
      # ====================== Welcome message ======================
      "welcome": "👋 Hello, welcome, {user}!\n\nI’m your personal reminder bot, projected by xyz-leo.\nI can send you scheduled messages to help you remember tasks, events, weather or anything important.\n\nPlease, type /help to check information and avaiable commands.",

      
      # ====================== Options menu message ======================
      # Options
      "option_weather": "🌤 See weather",
      "option_list_reminders": "📅 List reminders",
      "option_switch_language": "💬 Switch language",
      "option_help": "❓ Help",

      # Menu
      "options_menu": "😊 What do you want to do now?",
      "weather_menu": "If the state/city is not listed, type manually with /weather <city>. Example: /weather São Paulo\n\n🌤 Which state do you want to see the weather?",      
      #  ====================== language change message ======================
      "lang_change": "💬 Language set to American English, {lang}-US",
      "lang_change_error": "❗ Invalid language. Use 'pt' or 'en'.",
      
      
      # ====================== Weather ======================
      "weather": "🌤 The weather in {city} is '{description}' with temperature of {temp}°C.",
      "weather_not_city": "City not provided. Using 'São Paulo' as standard.",
      "weather_error": "❗ Could not obtain the weather for the specified city. '{city}'",


      # ====================== Reminders ======================
      "reminder_usage": "Usage:\n/reminder <HH:MM> <message>\nOR\n/reminder <HH:MM> /handler <param>. Example: /reminder 12:00 /weather Sao Paulo",
      "reminder_invalid_time": "❗ Invalid time format. Use HH:MM 24-hour format.",
      "reminder_scheduled": "📝 Reminder scheduled at {time}.",

      # List reminders
      "no_reminders": "You have no reminders.",
      "lsreminders": "📅 Here are your scheduled reminders:\n___________________________________________",
      "lsreminders_handler": "📨 Handler: {handler} {param}\n\n⏰ Time: {time}\n\n🆔: {sched_id}\n___________________________________________",
      "lsreminders_message": "📨 Message: {message}\n\n⏰ Time: {time}\n\n🆔: {sched_id}\n___________________________________________",

      #  Remove reminders
      "rmreminder_usage": "Usage: /rmreminder <schedule_id>",
      "rmreminder_not_found": "❗ No reminder found with ID {schedule_id}.",
      "rmreminder_removed": "🗑️ Reminder removed.",

      
      # ====================== Curiosity ======================
      "curiosity": "💡 Curiosity",
      "curiosity_message": "💡 Curiosity:\n\n{fact}",
      "curiosity_disclaimer": "⚠️ The curiosity may not be true. This command is just for fun.",
      "curiosity_error": "❗ Could not obtain a curiosity now.",

      
      # ====================== Translate ======================
      "translated_message": "🦜 Translated ({source} → {target}):\n\n{translated}",
      "translate_usage": "Usage: /translate <from> <to> <text>\nExample: /translate pt en Olá mundo!",

      
      # ====================== Cooldown message ======================
      "cooldown_message": "⏳ You are clicking too fast. Wait a few seconds before trying again.",
      

      # ====================== User Data ======================
      "userdata": "👤 User Data",
      "user_data": "👤 User Data\n___________________________________________\nName: {user_name}\nID: {user_id}\nLanguage: {lang}-US\n\nCommands requested:\n{commands}",

      
      # ====================== Unknown command message ======================
      "unknown": "❓ I didn’t understand. Type /help to see commands.",
  }
}

# --- Get message in user language ---
def bot_send_message(user_lang, key):
  """Returns message in the user language, or portuguese fallback"""
  return MESSAGES.get(user_lang, MESSAGES["pt"]).get(key, key)
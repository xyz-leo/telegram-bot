MESSAGES = {
  "pt": {
      # Help message
      "help_text": (
          "Olá, {user}!\n\n"
          "Todos os comandos começam com '/' e também possuem uma abreviação.\n\n"
          "Aqui estão os comandos disponíveis para este bot:\n\n"
          "• /st ou /start - Iniciar o bot e mostrar essa mensagem de ajuda.\n\n"
          "• /lg ou /language <pt|en> - Mudar idioma. Exemplo: /lg pt\n\n"
          "• /wt ou /weather <city> - Checar previsão do tempo em uma cidade. Exemplo: /weather Sao Paulo\n\n"
          "• /nw ou /news <topic> - Checar as notícias de um tópico ou categoria. Exemplo: /news esportes\n\n"
          "• /re ou /reminder <HH:MM> <message> - Agendar uma mensagem para ser enviada numa hora específica, todos os dias.\n\n"
          "• /lsre or /lsreminders - Listar todos os lembretes agendados.\n\n"
          "• /rmre or /rmreminder <schedule_id> - Remove um lembrete agendado pelo ID. você pode pegar o ID com o comando /lsreminders\n\n"
          "• /hp or /help - Mostra essa mensagem de ajuda.\n"
          #... add more commands as needed
      ),

      # Welcome message
      "welcome": "👋 Olá, seja bem-vindo, {user}!\n\nVocê pode digitar /help para consultar os comandos disponíveis.",

      # language change message
      "lang_change": "Idioma definido para português brasileiro, {lang}-br",
      "lang_help": "Digite /language <pt|en>, exemplo: /config pt",

      # Weather message
      "weather": "O clima em {city} está '{description}' com a temperatura de {temp}°C.",
      "weather_not_city": "Cidade não fornecida. Usando 'São Paulo' como padrão.",
      "weather_error": "Não foi possível obter o clima para a cidade especificada. '{city}'",

      # Unknown command message
      "unknown": "❓ Não entendi. Digite /help para ver os comandos",
  },
  "en": {
      # Help message
      "help_text": (
          "Hello, {user}!\n"
          "\nAll commands start with '/' and also have an abbreviation.\n\n"
          "Here is the available commands for this bot:\n\n"
          "• /st or /start - Start the bot and show this help message\n\n"
          "• /lg or /language <pt|en> - Change the language. Example: /lg pt\n\n"
          "• /wt or /weather <city> - Get current weather for a city. Example: /weather Sao Paulo\n\n"
          "• /nw or /news <topic> - Get the current news for a topic or category. Example: /news sports\n\n"
          "• /re or /reminder <HH:MM> <message> - Schedule a message to be sent at a specific time, everyday\n\n"
          "• /lsre or /lsreminders - List all scheduled reminders\n\n"
          "• /rmre or /rmreminder <schedule_id> - Remove a scheduled reminder by ID. You can get the ID with the command /lsreminders\n\n"
          "• /hp or /help - Show this help message\n"
          #... add more commands as needed
      ),

      # Welcome message
      "welcome": "👋 Hello, welcome, {user}!\n\nYou can type /help to check avaiable commands.",

      # language change message
      "lang_change": "Language set to American English, {lang}-us",
      "lang_help": "Type /language <pt|en>, example: /config en",

      # Weather message
      "weather": "The weather in {city} is '{description}' with temperature of {temp}°C.",
      "weather_not_city": "City not provided. Using 'São Paulo' as standard.",
      "weather_error": "Could not obtain the weather for the specified city. '{city}'",
      
      # Unknown command message
      "unknown": "❓ I didn’t understand. Type /help to see commands.",
  }
}

def bot_send_message(user_lang, key):
  """Retorna mensagem no idioma do usuário, ou fallback para inglês."""
  return MESSAGES.get(user_lang, MESSAGES["en"]).get(key, key)
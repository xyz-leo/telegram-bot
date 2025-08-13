# Telegram Reminder Bot

## Overview

This project is a Telegram bot implemented using the `python-telegram-bot` library. The bot allows users to schedule reminders that send messages or trigger predefined commands (handlers) at specified times daily. It supports multiple users, storing scheduled tasks persistently in a JSON file, and reloading them automatically when the bot restarts.

The bot also includes commands for getting weather information and news updates, which can be scheduled as reminders.

## IMPORTANT

When using the reminders, do not schedule anything sensitive, as this bot does not implement any cryptography or encryption for stored data or messages.

---

## Features

### 1. Scheduling Reminders

- Users can schedule reminders using the `/reminder` command.
- Reminders can be simple text messages or calls to predefined handlers such as weather or news.
- The scheduled reminders repeat daily at the specified time.
- Scheduled tasks are stored persistently in a JSON file (`reminders.json`) under each user's chat ID.
- On bot startup, all reminders are loaded from the JSON and scheduled automatically.
- Users can list their scheduled reminders with `/lsreminders`.
- Users can remove reminders by ID with `/rmreminder`, which deletes the reminder both from persistent storage and the bot’s job queue.

### 2. Handlers for Scheduled Tasks

- The bot supports running handlers as scheduled jobs. Examples include:
  - `/weather <city>`: Fetches current weather information for the specified city (default: São Paulo).
  - `/news <topic>`: Fetches news articles by category or search query.
- Handlers are invoked automatically when a scheduled reminder with a handler type is triggered.
- The bot uses a handler dictionary internally to map handler names to functions.
- Handlers internally use utility functions (`get_weather`, `get_news`) to retrieve data from third-party APIs.

### 3. Commands

- `/start` - Welcomes the user and displays available commands.
- `/help` - Shows help information listing available commands.
- `/language <lang>` - Switch between english and portuguese.
- `/weather <city>` - Fetches weather information for a given city.
- `/news <topic>` - Fetches news by category or keyword.
- `/reminder <HH:MM> <message>` - Schedule a simple message reminder at a specified 24-hour time.
- `/reminder <HH:MM> /handler <param>` - Schedule a reminder that triggers a handler with optional parameters.
- `/lsreminders` - Lists all active reminders for the user.
- `/rmreminder <schedule_id>` - Removes a scheduled reminder by its ID.

### 4. Language support

This bot supports both English and Brazilian Portuguese (pt-BR).
Users can switch between languages, and all bot messages, including responses from commands like /weather and /news, will be displayed in the selected language.

The language system is implemented using message templates with placeholders, allowing dynamic content (e.g., city names, temperatures) to be correctly formatted in either language.

Users language preferences are saved persistently in a JSON file, so the bot remembers the chosen language for future interactions.

---

## Architecture and Implementation Details

### Persistence

- Reminders are stored in a JSON file (`reminders.json`) organized by chat ID keys, allowing multiple users to have independent scheduled reminders.
- Each reminder entry stores:
  - Unique `id` (UUID string)
  - Scheduled `time` in `HH:MM` 24-hour format
  - `type` (either `"message"` or `"handler"`)
  - For handlers: `handler` name and optional `param`
  - For messages: the message text

### Scheduling

- Uses the `JobQueue` feature of `python-telegram-bot` to schedule jobs.
- Jobs run daily at the specified time (converted from local Brasília time to UTC internally).
- When the bot starts, it reads all reminders from the JSON file and schedules them with the job queue.
- When reminders are removed, the corresponding job(s) are also removed from the job queue immediately.
- Jobs are named using the pattern `<chat_id>_<schedule_id>_daily` to allow precise removal.

### Concurrency and Async

- All handlers and commands are implemented as asynchronous functions (`async def`) to integrate with the `python-telegram-bot` async framework.
- Network calls to external APIs (weather, news) are done synchronously inside utility functions but can be improved to async if needed.

### Modularity

- Commands and handlers are separated into modules (`handlers.py`, `utils.py`, `scheduler.py`).
- Handlers for scheduled jobs are dynamically dispatched using a dictionary to keep the scheduled message logic clean and extensible.
- Utility functions manage API interactions and JSON file persistence.

---

## Limitations and Notes

- The bot keeps scheduled jobs in memory; if the bot process restarts, jobs must be reloaded from the JSON file.
- Removing a reminder correctly cancels the job from the job queue, preventing further executions.
- Timezone handling is hardcoded to Brasília time (UTC-3) with conversion to UTC for scheduling.
- There is no user authentication beyond Telegram chat IDs.
- The JSON persistence is simple and may not scale well for a very large number of users or reminders.
- Error handling is minimal; improvements can be made to handle API failures or invalid user inputs more gracefully.
- Handlers are currently limited to weather and news but can be extended easily.

---

# - *- coding: utf- 8 - *-
import configparser
import asyncio
from datetime import datetime, timedelta

from bot.data.db import DB

# Создание экземпляра бд 
async def main_db():
    db = await DB()

    return db

BOT_TIMEZONE = "Europe/Moscow"  # Временная зона бота

loop = asyncio.get_event_loop()
task = loop.create_task(main_db())
db = loop.run_until_complete(task)

# Чтение конфига
read_config = configparser.ConfigParser()
read_config.read("settings.ini")

bot_token = read_config['settings']['token'].strip().replace(" ", "")  # Токен бота
path_database = "tgbot/data/database.db"  # Путь к Базе Данных


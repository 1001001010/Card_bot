# - *- coding: utf- 8 - *-
import configparser
from typing import Union
import time
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from datetime import datetime
import pytz

from bot.data.loader import bot
from bot.data.config import db, BOT_TIMEZONE

# Получение админов
def get_admins():
    read_admins = configparser.ConfigParser()
    read_admins.read("settings.ini")

    admins = read_admins['settings']['admin_id'].strip().replace(" ", "")

    if "," in admins:
        admins = admins.split(",")
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while "" in admins:
        admins.remove("")
    while " " in admins:
        admins.remove(" ")

    admins = list(map(int, admins))

    return admins

#Рассылка админам
async def send_admins(msg, photo=None, video=None, file=None):
    for admin in get_admins():
        if photo:
            await bot.send_photo(chat_id=admin, photo=photo, caption=msg)
        elif file:
            await bot.send_document(chat_id=admin, document=file, caption=msg)
        elif video:
            await bot.send_video(chat_id=admin, video=video, caption=msg)
        else:
            await bot.send_message(chat_id=admin, text=msg)
      
        
# Удаление отступов в многострочной строке ("""text""")
def ded(get_text: str) -> str:
    if get_text is not None:
        split_text = get_text.split("\n")
        if split_text[0] == "": split_text.pop(0)
        if split_text[-1] == "": split_text.pop()
        save_text = []

        for text in split_text:
            while text.startswith(" "):
                text = text[1:].strip()

            save_text.append(text)
        get_text = "\n".join(save_text)
    else:
        get_text = ""

    return get_text
    
# Преобразование числа в читаемый вид (123456789 -> 123 456 789)
def format_rate(amount: Union[float, int], around: int = 2) -> str:
    if "," in str(amount): amount = float(str(amount).replace(",", "."))
    if " " in str(amount): amount = float(str(amount).replace(" ", ""))
    amount = str(round(amount, around))

    out_amount, save_remains = [], ""

    if "." in amount: save_remains = amount.split(".")[1]
    save_amount = [char for char in str(int(float(amount)))]

    if len(save_amount) % 3 != 0:
        if (len(save_amount) - 1) % 3 == 0:
            out_amount.extend([save_amount[0]])
            save_amount.pop(0)
        elif (len(save_amount) - 2) % 3 == 0:
            out_amount.extend([save_amount[0], save_amount[1]])
            save_amount.pop(1)
            save_amount.pop(0)
        else:
            print("Error 4388326")

    for x, char in enumerate(save_amount):
        if x % 3 == 0: out_amount.append(" ")
        out_amount.append(char)

    response = "".join(out_amount).strip() + "." + save_remains

    if response.endswith("."):
        response = response[:-1]

    return response

# Получение даты
def get_date(full: bool = True) -> str:
    if full:  # Полная дата с временем
        return datetime.now(pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y %H:%M:%S")
    else:  # Только дата без времени
        return datetime.now(pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y")
    
# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.data.loader import bot
from bot.utils.utils_functions import get_admins

from bot.data.config import db

def send_photo(user_id):
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton("💌 Отправить скрины", callback_data="send_photo"))
    kb.append(InlineKeyboardButton("💌 Сообщения", callback_data="message_list"))
    kb.append(InlineKeyboardButton("📝 Изменить текст", callback_data="revork_text"))
    kb.append(InlineKeyboardButton("📩 Рассылка", callback_data="newsletter"))
    keyboard.add(kb[0])
    if user_id in get_admins(): 
        keyboard.add(kb[1], kb[2])
        keyboard.add(kb[3])

    return keyboard

#Возвращение в главное меню
def adm_back_main():
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton("🔙 Назад", callback_data="back_main_adm"))
    keyboard.add(kb[0])
    return keyboard


def kb_tip_newsletter():
   keyboard = InlineKeyboardMarkup()
   kb = []

   kb.append(InlineKeyboardButton("🖊️ Текст", callback_data=f"msg:text"))
   kb.append(InlineKeyboardButton("🖼️ Текст c фото", callback_data=f"msg:photo"))

   keyboard.add(kb[0], kb[1])
   keyboard.add(InlineKeyboardButton("🔙 Назад", callback_data=f"back_main_adm"))

   return keyboard

def back_tip_news():
   keyboard = InlineKeyboardMarkup()
   kb = []
   kb.append(InlineKeyboardButton("🔙 Назад", callback_data="newsletter"))
   keyboard.add(kb[0])
   return keyboard

def zayvka_full(id):
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton("🗑️ Удалить", callback_data=f"del:{id}"))
    keyboard.add(kb[0])

    return keyboard

def kb_skip():
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton("↪️ Пропустить", callback_data=f"skip"))
    keyboard.add(kb[0])

    return keyboard

async def group_list_open():
    keyboard = InlineKeyboardMarkup()
    kb = []
    code = await db.get_status_apl(status="sent")
    for btn in code:
        keyboard.add(InlineKeyboardButton(btn['user_id'], callback_data=f"open_group:{btn['id']}"))
    list_kb = [
        InlineKeyboardButton("Закрыть", callback_data="close_menu")
    ]
    keyboard.add(list_kb[0])

    return keyboard
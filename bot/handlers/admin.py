from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import types

from bot.data.loader import dp, bot
from bot.filters.filters import IsAdmin
from bot.data.config import db
from bot.keyboards.inline import group_list_open, zayvka_full, adm_back_main, kb_tip_newsletter, back_tip_news
from bot.state.admin import NewText, Newsletter, Newsletter_photo
from bot.utils.utils_functions import send_admins

from aiogram.dispatcher.middlewares import BaseMiddleware
import asyncio
from typing import  Union
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler

class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            return

        try:
            self.album_data[message.media_group_id].append(message)
            raise CancelHandler()  # Tell aiogram to cancel handler for this group element
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            message.conf["is_last"] = True
            data["album"] = self.album_data[message.media_group_id]

    async def on_post_process_message(self, message: types.Message, result: dict, data: dict):
        """Clean up after handling our album."""
        if message.media_group_id and message.conf.get("is_last"):
            del self.album_data[message.media_group_id]

#Рассылка
@dp.callback_query_handler(IsAdmin(), text="newsletter", state="*")
async def func_newsletter_tip(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Выберите тип рассылки", reply_markup=kb_tip_newsletter())
    
@dp.callback_query_handler(IsAdmin(), text_startswith="msg", state="*")
async def func_newsletter_msg(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    type_id = call.data.split(":")[1]
    if type_id == 'text':
        await call.message.answer("Введите текст рассылки", reply_markup=back_tip_news())
        await Newsletter.msg.set()
    elif type_id == 'photo':
        await call.message.answer("Введите текст рассылки", reply_markup=back_tip_news())
        await Newsletter_photo.msg.set()
    
@dp.message_handler(state=Newsletter_photo.msg)
async def func_newsletter_text(message: Message, state: FSMContext):
    msg = message.parse_entities()
    await state.update_data(msg=message.text)
    await message.answer("Отправьте фотографию для рассылки", reply_markup=adm_back_main())
    await Newsletter_photo.photo.set()
    
@dp.message_handler(IsAdmin(), content_types=['photo'], state=Newsletter_photo.photo)
async def mail_photo_starts(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
    data = await state.get_data()
    await send_admins(f"<b>❗ Администратор @{message.from_user.username} запустил рассылку!</b>")
    users = await db.all_users()
    yes_users, no_users = 0, 0
    for user in users:
        user_id = user['id']
        try:
            user_id = user['user_id']
            await bot.send_photo(chat_id=user_id, photo=data['photo'] ,caption=data['msg'])
            yes_users += 1
        except:
            no_users += 1

    new_msg = f"""
<b>💎 Всего пользователей: <code>{len(await db.all_users())}</code>
✅ Отправлено: <code>{yes_users}</code>
❌ Не отправлено (Бот заблокирован): <code>{no_users}</code></b>
    """

    await message.answer(new_msg)
    await state.finish()
    
@dp.message_handler(state=Newsletter.msg)
async def func_newsletter_text(message: Message, state: FSMContext):
    await state.update_data(msg=message.text)
    data = await state.get_data()
    await send_admins(f"<b>❗ Администратор @{message.from_user.username} запустил рассылку!</b>")
    users = await db.all_users()
    yes_users, no_users = 0, 0
    for user in users:
        user_id = user['id']
        try:
            user_id = user['user_id']
            await bot.send_message(chat_id=user_id, text=data['msg'])
            yes_users += 1
        except:
            no_users += 1

    new_msg = f"""
<b>💎 Всего пользователей: <code>{len(await db.all_users())}</code>
✅ Отправлено: <code>{yes_users}</code>
❌ Не отправлено (Бот заблокирован): <code>{no_users}</code></b>
    """

    await message.answer(new_msg)
    await state.finish()

#Открытие меню
@dp.callback_query_handler(IsAdmin(), text='revork_text', state="*")
async def func_name__work(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Введите новый текст для стартового сообщения, можете использовать Telegram разметку")
    await NewText.text.set()

@dp.message_handler(IsAdmin(), state=NewText.text)
async def func_newsletter_text(message: Message, state: FSMContext):
    msg = message.parse_entities()
    await db.update_text(id=1, start_text=msg)
    await message.answer("Текст успешно изменен")
    await state.finish()
    
@dp.callback_query_handler(IsAdmin(), text='message_list', state="*")
async def func_name__work(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Список заявок", reply_markup=await group_list_open())

@dp.callback_query_handler(IsAdmin(), text_startswith='open_group', state="*")
async def func_name__work(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    open_id = call.data.split(":")[1]
    db_info = await db.get_info_apl(id=open_id)
    list_photo = [db_info['first_photo'], db_info['second_photo'], db_info['third_photo'], db_info['fourth_photo'], db_info['fifth_photo']]
    album = []
    user_info = await db.get_user(user_id=db_info['user_id'])
    if user_info['user_name'] == "":
        us = await bot.get_chat(user_info['user_id'])
        name = us.get_mention(as_html=True)
    else:
        name = user_info['user_name']
    text = f"{db_info['text_photo']}\n\n<b>Пользователь</b> @{name}"
    for i in list_photo:
        if i is not None:
            album.append({"media": i, "type": 'photo'})
    if len(album) == 1:
        await bot.send_photo(call.from_user.id, album[0]['media'], caption=text, reply_markup=zayvka_full(id=open_id))
    else:
        media_group = types.MediaGroup()
        for obj in album:
            try:
                media_group.attach(types.InputMediaPhoto(media=obj['media']))
            except ValueError:
                return await call.message.answer("This type of album is not supported by aiogram.")
        msg = await bot.send_media_group(call.from_user.id, media=media_group)
        await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=zayvka_full(id=open_id))
        
@dp.callback_query_handler(IsAdmin(), text_startswith='del', state="*")
async def func_name__work(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    del_id = call.data.split(":")[1]
    await db.del_appl(id=del_id, status='verified')
    await call.message.answer("Список заявок", reply_markup=await group_list_open())
    
@dp.callback_query_handler(IsAdmin(), text='close_menu', state="*")
async def func_name__work(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
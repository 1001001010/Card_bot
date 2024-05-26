from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.data.config import db
from bot.data.loader import dp, bot
from bot.state.admin import SendPhoto
from bot.utils.utils_functions import get_admins
from bot.keyboards.inline import send_photo, kb_skip

import asyncio
from typing import List, Union
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import CancelHandler

#Обработка команды /start
@dp.message_handler(commands=['start'], state="*")
async def func_main_start(message: Message, state: FSMContext):
    await state.finish()
    texts = await db.get_text()
    for text in texts:
        await bot.send_message(message.from_user.id, text['start_text'], reply_markup=send_photo(user_id=message.from_user.id))

@dp.callback_query_handler(text='back_main_adm', state="*")
async def func_name__work(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()
    texts = await db.get_text()
    for text in texts:
        await bot.send_message(call.from_user.id, text['start_text'], reply_markup=send_photo(user_id=call.from_user.id))
        
@dp.callback_query_handler(text='skip', state="*")
async def func_name__work(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Отправьте сообщение для тс`а')
    await SendPhoto.Photo_text.set()
    
@dp.callback_query_handler(text='send_photo', state="*")
async def func_name__work(call: CallbackQuery, state: FSMContext):
    info = await db.get_status_apl(user_id=call.from_user.id, status='sent')
    if info:
        await call.message.answer("Дождитесь отработки предыдущей заявки")
    else:
        await state.finish()
        await call.message.edit_text('Вам необходимо отправить 5 фото\nОтправьте первое фото')
        await SendPhoto.Photo1.set()
        
@dp.message_handler(content_types=['photo'], state=SendPhoto.Photo1)
async def func_new__photo__work(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(Photo1=photo)
    await state.update_data(Photo2=None)
    await state.update_data(Photo3=None)
    await state.update_data(Photo4=None)
    await state.update_data(Photo5=None)
    await message.answer('Отправьте второе фото', reply_markup=kb_skip())
    await SendPhoto.Photo2.set()
    
@dp.message_handler(content_types=['photo'], state=SendPhoto.Photo2)
async def func_new__photo__work(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(Photo2=photo)
    await message.answer('Отправьте третье фото', reply_markup=kb_skip())
    await SendPhoto.Photo3.set()
    
@dp.message_handler(content_types=['photo'], state=SendPhoto.Photo3)
async def func_new__photo__work(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(Photo3=photo)
    await message.answer('Отправьте четвертое фото', reply_markup=kb_skip())
    await SendPhoto.Photo4.set()
    
@dp.message_handler(content_types=['photo'], state=SendPhoto.Photo4)
async def func_new__photo__work(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(Photo4=photo)
    await message.answer('Отправьте пятое фото', reply_markup=kb_skip())
    await SendPhoto.Photo5.set()
    
@dp.message_handler(content_types=['photo'], state=SendPhoto.Photo5)
async def func_new__photo__work(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(Photo5=photo)
    await message.answer('Отправьте сообщение для тс`а')
    await SendPhoto.Photo_text.set()
    
@dp.message_handler(state=SendPhoto.Photo_text)
async def func_source__work(message: Message, state: FSMContext):
    await state.update_data(Photo_text=message.text)
    data = await state.get_data()
    await db.new_applications(user_id=message.from_user.id, first_photo=data['Photo1'], second_photo=data['Photo2'], third_photo=data['Photo3'], fourth_photo=data['Photo4'], fifth_photo=data['Photo5'], text_photo=data['Photo_text'], status='sent')
    admins = get_admins()
    for admin in admins:
        await bot.send_message(admin, f"Новая заявка от пользователя @{message.from_user.username}")
    await message.answer("ваша заявка отправлена")
from aiogram.dispatcher.filters.state import State, StatesGroup


class NewText(StatesGroup): #State на добавление стартового текста
    text = State()
    
class SendPhoto(StatesGroup): #State на отправку фото
    Photo1 = State()
    Photo2 = State()
    Photo3 = State()
    Photo4 = State()
    Photo5 = State()
    Photo_text = State()
    
class Newsletter(StatesGroup): #State на рассылку
    msg = State()
    
class Newsletter_photo(StatesGroup): #State на рассылку с офто
    msg = State()
    photo = State()
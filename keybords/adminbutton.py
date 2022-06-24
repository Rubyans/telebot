from aiogram.types import ReplyKeyboardMarkup,KeyboardButton




button_load=KeyboardButton('/Завантажити')
button_delete=KeyboardButton('/Видалити')

buttonadmin=ReplyKeyboardMarkup(resize_keyboard=True).add(button_load,button_delete)

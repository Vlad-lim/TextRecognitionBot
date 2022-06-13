from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_proc = KeyboardButton('Обработка')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_proc)
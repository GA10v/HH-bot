from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

Button_1 = KeyboardButton('/run')
Button_2 = KeyboardButton('/like')
Button_3 = KeyboardButton('/help')
Button_4 = KeyboardButton('/send')

client_kb = ReplyKeyboardMarkup(resize_keyboard=True)
client_kb.add(Button_1).add(Button_2).add(Button_3).add(Button_4)

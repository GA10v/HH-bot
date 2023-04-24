from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

Button_1 = KeyboardButton('/dump_hh')
Button_2 = KeyboardButton('/update_db')
Button_3 = KeyboardButton('/end')

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb.add(Button_1).add(Button_2).add(Button_3)

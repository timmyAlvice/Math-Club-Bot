# from aiogram.types import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup

task_button = KeyboardButton(text="Решить задачу")
other_button = KeyboardButton(text="Режим 2")

choose_mode_kb = ReplyKeyboardMarkup(keyboard=[[task_button, other_button]], resize_keyboard=True)

# choose_mode_kb.add(model_button).add(database_button)
# from aiogram.types import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup

task_button = KeyboardButton(text="Решить задачу")
test_button = KeyboardButton(text="Решить тест")
profile_button = KeyboardButton(text="Профиль")
info_button = KeyboardButton(text="Как пользоваться?")
about_button = KeyboardButton(text="О проекте", )

choose_mode_kb = ReplyKeyboardMarkup(
    keyboard=[
        [task_button, test_button], 
        [profile_button, info_button],
        [about_button]
    ], 
    resize_keyboard=True
)
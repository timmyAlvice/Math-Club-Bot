import asyncio
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import State, StatesGroup
from aiogram import Router, F
from create_bot import bot
from keyboards import back_to_menu_kb
from utils import get_response
from handlers.menu_handlers import ModeStates

problem_mode_router = Router()

@problem_mode_router.callback_query(
    ModeStates.task_mode, 
    F.data.contains("problem")
)
async def start_test(
    message: types.Message, 
    state=FSMContext
) -> None:
    
    await bot.send_message(
        message.from_user.id,
        text="Найдите точку минимума функции y = x^3 - 27x на отрезке [0, 4]"
    )


@problem_mode_router.message(
    ModeStates.task_mode, 
    F.text
)
async def task_response_handler(
        message: types.Message, 
        state: FSMContext
    ) -> None: 

    chat_id = message.from_user.id
        
    load_message = await bot.send_message(
        chat_id=chat_id,
        text="Анализируем решение..." 
    )

    model_response = await get_response(message.text)
    
    await bot.send_message(
        chat_id=chat_id,
        text=model_response,
        reply_markup=back_to_menu_kb
    )

    await bot.delete_message(
        chat_id=chat_id,
        message_id=load_message.message_id
    )
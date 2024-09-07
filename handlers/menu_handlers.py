import asyncio
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import State, StatesGroup
from aiogram import Router, F
from create_bot import bot

from keyboards import (
    choose_mode_kb, 
    back_to_menu_kb, 
    get_tasks_kb
)

from utils import (
    WELCOME_MESSAGE,
    PROBLEM_MODE_MESSAGE, 
    CHOOSE_TASK_MESSAGE,
    TEST_MODE_MESSAGE, 
    PROFILE_MODE_MESSAGE, 
    INFO_MODE_MESSAGE, 
    get_response
)

menu_router = Router()

class ModeStates(StatesGroup):
    task_mode = State()
    test_mode = State()
    profile_mode = State()
    info_mode = State()


async def send_menu_message(
        message: types.Message,
        delete_previous: bool=True
    ) -> None:

    chat_id = message.from_user.id

    choose_message = await bot.send_message(
        chat_id=chat_id,
        text="Выберете режим:",
        reply_markup=choose_mode_kb
    )

    if delete_previous:
        await bot.delete_message(
            chat_id=chat_id,
            message_id=choose_message.message_id - 1
        )


async def send_return_message(
        message: types.Message
    ) -> None:

    await bot.send_message(
        chat_id=message.from_user.id,
        text="Ну что, давай решать?",
        reply_markup=back_to_menu_kb
    )


@menu_router.message(Command(commands=["start", "help"]))
async def start_chat(
    message: types.Message, 
    state: FSMContext
) -> None:

    await state.clear()

    await bot.send_message(
        chat_id=message.from_user.id,
        text=WELCOME_MESSAGE
    )

    await send_menu_message(
        message=message, 
        delete_previous=False
    )

    await message.delete()


@menu_router.callback_query(F.data == "to_menu")
async def menu_message_handler(
    message: types.Message, 
    state: FSMContext
) -> None:
    
    await state.clear()
    await send_menu_message(message)


@menu_router.message(F.text.lower() == "решить задачу")
async def set_task_mode(
        message: types.Message, 
        state: FSMContext
    ) -> None:

    chat_id = message.from_user.id
    
    await state.set_state(ModeStates.task_mode)
    await bot.send_message(
        chat_id=chat_id,
        text=PROBLEM_MODE_MESSAGE,
        reply_markup=types.ReplyKeyboardRemove()
    )

    await bot.send_message(
        chat_id=chat_id,
        text=CHOOSE_TASK_MESSAGE,
        reply_markup=get_tasks_kb(
            mode="problem"
        )
    )


@menu_router.message(F.text.lower() == "решить тест")
async def set_other_mode(
        message: types.Message, 
        state: FSMContext
    ) -> None:

    chat_id = message.from_user.id
    
    await state.set_state(ModeStates.test_mode)    
    await bot.send_message(
        chat_id=chat_id,
        text=TEST_MODE_MESSAGE,
        reply_markup=types.ReplyKeyboardRemove()
    )

    await bot.send_message(
        chat_id=chat_id,
        text=CHOOSE_TASK_MESSAGE,
        reply_markup=get_tasks_kb(
            mode="test"
        )
    )


@menu_router.message(F.text.lower() == "профиль")
async def set_other_mode(
        message: types.Message, 
        state: FSMContext
    ) -> None:

    chat_id = message.from_user.id
    user_name = str(message.from_user.full_name)
    
    await state.set_state(ModeStates.profile_mode)    
    await bot.send_message(
        chat_id=chat_id,
        text=PROFILE_MODE_MESSAGE.format(name=user_name),
        reply_markup=types.ReplyKeyboardRemove()
    )

    await send_return_message(message)


@menu_router.message(F.text.lower() == "как пользоваться?")
async def set_other_mode(
        message: types.Message, 
        state: FSMContext
    ) -> None:

    chat_id = message.from_user.id
    
    await state.set_state(ModeStates.info_mode)    
    await bot.send_message(
        chat_id=chat_id,
        text=INFO_MODE_MESSAGE,
        reply_markup=types.ReplyKeyboardRemove()
    )

    await send_return_message(message)


    
@menu_router.message(ModeStates.task_mode, F.text)
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

@menu_router.message(F.photo)
async def handle_photo(message: types.Message):
    # Получаем file_id из фото
    file_id = message.photo[-1].file_id  # Берем максимальное качество фото
    await message.answer(f"Ваш file_id: `{file_id}`")
import asyncio, os, requests
from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
# from aiogram.filters import Text
from aiogram.filters.command import Command
from aiogram.filters.base import Filter
from aiogram.filters.state import State, StatesGroup
from aiogram import Router, F

# from create_bot import bot
from keyboards import choose_mode_kb #, get_docs_kb, feedback_kb
from utils import WELCOME_MESSAGE, \
      get_response

router = Router()

class ModeStates(StatesGroup):
    task_mode = State()
    other_mode = State()

@router.message(Command("start"))
async def start_chat(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=WELCOME_MESSAGE, 
        reply_markup=choose_mode_kb
    )
    await message.delete()

# ======================== MODEL HANDLERS ========================

@router.message(F.text.lower() == "решить задачу")
async def set_task_mode(
        message: types.Message, 
        state: FSMContext
    ) -> None:

    await state.set_state(ModeStates.task_mode)
    await message.answer(
        text="Найдите наименьшее значение функции y = x^3 - 27x на отрезке [0; 4]"
    ) 
    
    
@router.message(ModeStates.task_mode, F.text)
async def task_response_handler(
        message: types.Message, 
        state: FSMContext
    ) -> None:
    
    try:   
        await message.answer(
            text="Анализируем решение..." 
        )
        
        model_response = await get_response(message.text)
        
        await message.answer(
            text=model_response, 
            # reply_markup=get_docs_kb
        )
            
    except Exception as e:
        await message.answer(
            text=f"An error occurred: {str(e)}", 
            # reply_markup=get_docs_kb
        )
        
    
# async def send_links(callback_query: types.CallbackQuery):
    
#     for doc in content:
#         await bot.send_message(
#             chat_id=callback_query.from_user.id, 
#             text=doc
#         )

# ======================== DATABASE HANDLERS ========================

@router.message(F.text.lower() == "режим 2")
async def set_other_mode(
        message: types.Message, 
        state: FSMContext
    ) -> None:

    await state.set_state(ModeStates.other_mode)
    await message.answer(text="Другой режим:")
    
# async def get_database_response(message: types.Message, state: FSMContext):    
    
#     try:
#         database_response = await get_docs_from_api(message.text)
        
#         for doc in database_response:
#             await bot.send_message(
#                 chat_id=message.from_user.id, 
#                 text=doc
#             )
        
#     except Exception as e:
#         await bot.send_message(
#             chat_id=message.from_user.id, 
#             text=f"An error occurred: {str(e)}"
#         )


# def register_handlers(dp: Dispatcher):
#     dp.register_message_handler(
#         start_chat, 
#         commands=["start", "help"]
#     )

#     dp.register_message_handler(
#         set_task_mode, 
#         Filter(equals="Решить задачу", ignore_case=True), 
#         state='*'
#     )
    
#     dp.register_message_handler(
#         set_other_mode, 
#         Filter(equals="Режим 2", ignore_case=True), 
#         state='*'
#     )
    
#     # dp.register_callback_query_handler(
#     #     send_links, 
#     #     lambda callback: callback.data == "get_docs",
#     #     state=ModeStates.model_mode
#     # )
    
#     dp.register_message_handler(
#         task_response_handler, 
#         state=ModeStates.model_mode
#     )
    
    # dp.register_message_handler(
    #     get_database_response, 
    #     state=ModeStates.database_mode
    # )
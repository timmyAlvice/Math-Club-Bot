import asyncio
from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, F

from create_bot import bot
from llm import giga_llm
from utils import COMPARE_LLM_PROMPT
from keyboards import back_to_menu_kb
from utils import get_response, extract_text_in_brackets
from handlers.menu_handlers import ModeStates
from problem_generators import generate_quadratic_problem
import os

problem_mode_router = Router()
problem_storage = MemoryStorage()

class ProblemStates(StatesGroup):
    waiting_for_solution = State()
    # waiting_for_answer = State()
    problem_completed = State()
    

@problem_mode_router.callback_query(
    # ModeStates.task_mode, 
    F.data.contains("problem")
)
async def start_problem(
    message: types.Message, 
    state=FSMContext
) -> None:
    
    await state.set_state(ProblemStates.waiting_for_solution)
    
    function, answer, solution_explanation = generate_quadratic_problem()
    problem = f"Найдите критические точки функции" # \n```Math\n{function}```

    await state.update_data(
        problem=problem,
        answer=answer,
        solution_explanation=solution_explanation,
    )

    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=types.FSInputFile(f'{os.getcwd()}/tmp.png'),
        caption=problem,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    
    # await bot.send_message(
    #     message.from_user.id,
    #     text=problem,
    #     parse_mode=ParseMode.MARKDOWN_V2
    # )
    
    await bot.send_message(
        message.from_user.id,
        text="Введите решение в тестовом формате:"
    )
    
    
# def is_answer_correct(text):
#     text = text.lower()
    
#     if text.endswith("ответ: верный"):
#         return True
    
#     elif text.endswith("ответ: не верный"):
#         return False
    
#     else:
#         return None


@problem_mode_router.message(
    ProblemStates.waiting_for_solution
)
async def problem_response_handler(
        message: types.Message, 
        state: FSMContext
    ) -> None: 

    chat_id = message.from_user.id
    user_solution = message.text
        
    load_message = await bot.send_message(
        chat_id=chat_id,
        text="Искусственный интеллект анализирует ваше решение..." 
    )
    
    data = await state.get_data()
    problem = data.get("problem")
    answer = data.get("answer")
    solution_explanation = data.get("solution_explanation")
    
    prompt = COMPARE_LLM_PROMPT.format(
        problem=problem,
        answer=answer,
        solution_explanation=solution_explanation,
        user_solution=user_solution
    )

    model_response = await giga_llm.generate_text(prompt)
    processed_response = extract_text_in_brackets(model_response)

    print(processed_response)
    
    await bot.send_message(
        chat_id=chat_id,
        text=processed_response,
        reply_markup=back_to_menu_kb,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    
    # if is_answer_correct(model_response):
    #     await bot.send_message(
    #         chat_id=chat_id,
    #         text="Поздравляем! Ты заработал 100 очков!",
    #         reply_markup=back_to_menu_kb
    #     )
        
    # else:
    #     await bot.send_message(
    #         chat_id=chat_id,
    #         text="Не расстраивайся! Не ошибается только тот, кто не готовится к экзаменам!",
    #         reply_markup=back_to_menu_kb
    #     )

    await bot.delete_message(
        chat_id=chat_id,
        message_id=load_message.message_id
    )
    
    await state.set_state(ProblemStates.problem_completed)
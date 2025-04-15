import asyncio
from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, F

from create_bot import bot
from llm import llm
from utils import PROBLEM_PROMPT_TEMPLATE
from keyboards import back_to_menu_kb
from utils import get_response, extract_text_in_brackets
from handlers.menu_handlers import ModeStates
from problem_generators import generate_quadratic_problem
import os

problem_mode_router = Router()
problem_storage = MemoryStorage()

class ProblemStates(StatesGroup):
    waiting_for_solution = State()
    problem_completed = State()
    

@problem_mode_router.callback_query(
    F.data.contains("problem")
)
async def start_problem(
    message: types.Message, 
    state=FSMContext
) -> None:
    
    await state.set_state(ProblemStates.waiting_for_solution)
    
    function, answer, solution_explanation = generate_quadratic_problem()
    problem = f"Найдите критическую точку функции" # \n```Math\n{function}```
    problem_for_state = problem + f"\nf(x) = {function}"

    await state.update_data(
        problem=problem_for_state,
        answer=answer,
        solution_explanation=solution_explanation,
    )

    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=types.FSInputFile(f'{os.getcwd()}/tmp.png'),
        caption=problem,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    
    await bot.send_message(
        message.from_user.id,
        text="Введите решение в тестовом формате:"
    )


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
    
    prompt = PROBLEM_PROMPT_TEMPLATE.format(
        problem=problem,
        answer=answer,
        solution_explanation=solution_explanation,
        user_solution=user_solution
    )

    model_response = await llm.generate_text(prompt)
    print(f"\n\nMODEL RESPONSE:\n{model_response}")
    processed_response = extract_text_in_brackets(model_response)

    await bot.send_message(
        chat_id=chat_id,
        text=processed_response,
        reply_markup=back_to_menu_kb,
        parse_mode=ParseMode.MARKDOWN_V2
    )

    await bot.delete_message(
        chat_id=chat_id,
        message_id=load_message.message_id
    )
    
    await state.set_state(ProblemStates.problem_completed)
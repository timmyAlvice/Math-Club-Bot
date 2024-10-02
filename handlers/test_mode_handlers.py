import asyncio, logging
from aiogram import types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from create_bot import bot

from keyboards import back_to_menu_kb, end_test_kb
from test_generators import TestQuestionGenerator

test_mode_router = Router()
test_storage = MemoryStorage()

class TestStates(StatesGroup):
    waiting_for_answer = State()
    test_completed = State()

@test_mode_router.callback_query(F.data.contains("test"))
async def start_test(
    message: types.Message, 
    state=FSMContext
) -> None:
    
    await state.set_state(TestStates.waiting_for_answer)

    test_object = TestQuestionGenerator(10)
    questions = test_object.questions
    await state.update_data(questions=questions)

    await ask_question(
        chat_id=message.from_user.id, 
        questions=questions,
        question_index=0, 
        score=0, 
        state=state
    )


async def ask_question(
    chat_id: int, 
    questions: list[dict],
    question_index: int, 
    score: int, 
    state: FSMContext
) -> None:
    
    if question_index < len(questions):

        # user_data = await state.get_data()
        # questions = user_data.get('questions') 

        question = questions[question_index]
        print(f"\n\n{question}\n\n")

        # await bot.send_photo(
        #     chat_id=chat_id,
        #     photo=question["question"]
        # )

        poll_message = await bot.send_poll(
            chat_id=chat_id,
            question=question["question"],
            options=question["answers"],
            type='quiz',
            is_anonymous=False,
            correct_option_id=question["correct"],
            explanation="Выбери один вариант ответа",
            reply_markup=back_to_menu_kb
        )

        await state.update_data(
            current_question_index=question_index, 
            poll_id=poll_message.poll.id,
            score=score
        )

    else:
        await state.set_state(TestStates.test_completed)
        await bot.send_message(
            chat_id=chat_id, 
            text=f"Тест завершен! Ты набрал {score} из {len(questions)}."
        )

        result_text = "Поздравляем! Ты прошёл тему! 🥳" \
            if score >= 7 \
            else "Пока не хватает верных ответов 😔\nПопробуй ещё раз!"

        await bot.send_message(
            chat_id=chat_id, 
            text=result_text,
            reply_markup=end_test_kb
        )


@test_mode_router.poll_answer(TestStates.waiting_for_answer)
async def handle_poll_answer(
    poll_answer: types.PollAnswer, 
    state: FSMContext
) -> None:
        
    user_id = poll_answer.user.id
    data = await state.get_data()
    score = data.get('score', 0)
    questions = data.get('questions') 

    current_question_index = data.get('current_question_index')
    correct_index = questions[current_question_index]["correct"]
    
    if poll_answer.option_ids[0] == correct_index:
        score += 1

    await state.update_data(score=score)
    await ask_question(
        questions=questions,
        chat_id=user_id, 
        question_index=current_question_index + 1, 
        score=score, 
        state=state
    )
import asyncio, logging
from aiogram import types
from aiogram.filters.state import State, StatesGroup
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from create_bot import bot

from keyboards import back_to_menu_kb, end_test_kb
from utils import test_12 as questions
from utils import OPTIONS

test_mode_router = Router()

class TestStates(StatesGroup):
    waiting_for_answer = State()
    test_completed = State()


@test_mode_router.callback_query(F.data == "test12")
async def start_test(
    message: types.Message, 
    state=FSMContext
) -> None:
    
    await state.set_state(TestStates.waiting_for_answer)
    await ask_question(message.from_user.id, 0, 0, state)


async def ask_question(
    chat_id: int, 
    question_index: int, 
    score: int, 
    state: FSMContext
) -> None:
    
    if question_index < len(questions):

        question = questions[question_index]
        options = OPTIONS

        await bot.send_photo(
            chat_id=chat_id,
            photo=question["question"]
        )

        poll_message = await bot.send_poll(
            chat_id=chat_id,
            question="Выбери один вариант ответа:",
            options=OPTIONS,
            type='quiz',
            is_anonymous=False,
            correct_option_id=question["answer"],
            explanation="Спешка и невнимательность - худшие враги на экзаменах!",
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
    current_question_index = data.get('current_question_index')
    correct_index = questions[current_question_index]["answer"]
    
    if poll_answer.option_ids[0] == correct_index:
        score += 1

    await state.update_data(score=score)
    await ask_question(
        chat_id=user_id, 
        question_index=current_question_index + 1, 
        score=score, 
        state=state
    )
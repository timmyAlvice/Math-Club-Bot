from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

back_button = InlineKeyboardButton(
    text="В меню", 
    callback_data="to_menu"
)

back_to_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[[back_button]]
)

try_again_button = InlineKeyboardButton(
    text="Попробовать снова",
    callback_data="test12"
)

end_test_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [try_again_button],
        [back_button]
    ]
)


def get_tasks_kb(
        mode: str="problem",
        count: int=12
    ) -> InlineKeyboardMarkup:

    assert mode in {"problem", "test"}

    buttons = []

    for i in range(1, count + 1):
        text = str(i)
        callback = mode+text
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=callback
        ))

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            buttons[:4],
            buttons[4:8],
            buttons[8:],
            [back_button]
        ]
    )

    return kb

            
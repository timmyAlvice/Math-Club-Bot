# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# EXPIRE_TIME = None

# # get_docs inline keyboard
# get_docs_kb = InlineKeyboardMarkup(row_width=1)
# docs_button = InlineKeyboardButton(
#     text="Источники из документации", 
#     callback_data="get_docs", 
#     expire=EXPIRE_TIME
# )
# get_docs_kb.add(docs_button)

# # feedback inline keyboard
# feedback_kb = InlineKeyboardMarkup(row_width=2)
# like_button = InlineKeyboardButton(
#     text='👍', 
#     callback_data="like", 
#     expire=EXPIRE_TIME
# )
# dislike_button = InlineKeyboardButton(
#     text='👎', 
#     callback_data="dislike", 
#     expire=EXPIRE_TIME
# )
# feedback_kb.row(like_button, dislike_button)
from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.helpers.keyboards.question import \
    get_keyboard_question
from src.tgbot_expenses.states.states_chat import StateChat


@Bot.callback_query_handler(text="make_expenses", state=StateChat.MainMenu)
async def callbacks_make_expenses(query: types.CallbackQuery,
                                  state: FSMContext) -> None:
    """
   The process of starting to fill in expenses.
    """
    await query.message.delete()
    
    await StateChat.Category.set()

    await Bot.answer(
        message=query.message,
        text=QuestionText.category,
        reply_markup=get_keyboard_question(
            button_names=database.get_all_categories(),
            button_back=True
        )
    )

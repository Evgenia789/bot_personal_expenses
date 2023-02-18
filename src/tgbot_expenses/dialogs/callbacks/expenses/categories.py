from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.helpers.keyboards.question import get_keyboard_question
from src.tgbot_expenses.states.chat_states import StateChat


@Bot.callback_query_handler(state=StateChat.Category)
async def callbacks_get_category(query: types.CallbackQuery,
                                 state: FSMContext) -> None:
    """
    The process of selecting a category.
    """
    await query.message.delete()

    async with state.proxy() as data:
        data["category"] = query.data

    await StateChat.next()

    await Bot.answer(
        message=query.message,
        text=QuestionText.bill,
        reply_markup=get_keyboard_question(
            button_names=database.get_all_bills()
        )
    )

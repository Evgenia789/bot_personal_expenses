from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.callbacks.start_or_continue import (
    callbacks_continue, callbacks_start_over)
from src.tgbot_expenses.helpers.keyboards.question import \
    get_keyboard_question
from src.tgbot_expenses.states.states_chat import StateChat


@Bot.callback_query_handler(state=StateChat.Category)
async def callbacks_category(query: types.CallbackQuery,
                             state: FSMContext) -> None:
    """
    Process category button.
    """
    await query.message.delete()
    async with state.proxy() as data:
        data["category"] = query.data

    await StateChat.next()

    buttons_text = database.get_all_bills()
    
    await Bot.answer(
        query.message,
        QuestionText.bill,
        reply_markup=get_keyboard_question(button_names=buttons_text)
    )

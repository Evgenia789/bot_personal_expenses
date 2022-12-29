from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.callbacks.start_or_continue import (
    callbacks_continue, callbacks_start_over)
from src.tgbot_expenses.states.states_chat import StateChat


@Bot.callback_query_handler(state=StateChat.Bill)
async def callbacks_bill(query: types.CallbackQuery,
                         state: FSMContext) -> None:
    """
    Process bill button.
    """
    await query.message.delete()

    async with state.proxy() as data:
        data["bill"] = query.data

    await StateChat.next()

    await Bot.answer(query.message, QuestionText.amount)

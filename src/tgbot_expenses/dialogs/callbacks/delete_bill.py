from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.callbacks.start_or_continue import (
    callbacks_continue, callbacks_start_over)
from src.tgbot_expenses.helpers.keyboards.question import \
    get_keyboard_question
from src.tgbot_expenses.helpers.keyboards.question import \
    get_keyboard_question
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.callback_query_handler(text="delete_bill", state=StateSettings.ChangeBill)
async def callbacks_settings(query: types.CallbackQuery,
                             state: FSMContext) -> None:
    """
    Process of deleting a bill.
    """
    await query.message.delete()

    await StateSettings.DeleteBill.set()
    
    await Bot.answer(
        query.message,
        QuestionText.archive_bill,
        reply_markup=str(get_keyboard_question(database.get_all_bills(), button_back=True))
    )

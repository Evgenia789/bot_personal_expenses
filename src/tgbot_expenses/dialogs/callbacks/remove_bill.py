import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.callbacks.start_or_continue import (
    callbacks_continue, callbacks_start_over)
from src.tgbot_expenses.helpers.keyboards.back_or_main_menu import \
    get_keyboard_back_or_main_menu
from src.tgbot_expenses.dialogs.commands.start import send_welcome
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.callback_query_handler(state=StateSettings.DeleteBill)
async def callbacks_archive_bill(query: types.CallbackQuery,
                                 state: FSMContext) -> None:
    """
    Process archive the bill.
    """
    await query.message.delete()

    archive_bill = query.data

    await StateSettings.next()

    database.archive_bill(bill_name=archive_bill)

    last_message = await Bot.answer(
        query.message,
        QuestionText.result_archive
    )

    await asyncio.sleep(2)

    await send_welcome(last_message, state)

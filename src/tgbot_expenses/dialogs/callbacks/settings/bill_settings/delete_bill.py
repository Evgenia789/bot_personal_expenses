import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.commands.start import send_welcome
from src.tgbot_expenses.states.chat_states import StateSettings


@Bot.callback_query_handler(state=StateSettings.DeleteBill)
async def callbacks_delete_bill(query: types.CallbackQuery,
                                state: FSMContext) -> None:
    """
    The process of deleting a bill.
    """
    await query.message.delete()

    await StateSettings.next()

    database.archive_bill(bill_name=query.data)

    last_message = await Bot.answer(
        message=query.message,
        text=QuestionText.result_archive
    )

    await asyncio.sleep(2)

    await send_welcome(message=last_message, state=state)

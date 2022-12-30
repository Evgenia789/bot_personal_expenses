import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.commands.start import send_welcome
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.message_handler(state=StateSettings.AddBill, content_types=types.ContentType.ANY)
async def message_input_new_bill(message: types.Message, state: FSMContext) -> None:
    """
    Process of input a new bill.
    """
    await Bot.delete_messages(chat_id=message.chat.id,
                              last_message_id=message.message_id, count=2)

    await StateSettings.next()

    database.insert_account(account_name=message.text)

    message = await Bot.answer(
        message=message,
        text=f"Account {message.text} added"
    )

    await asyncio.sleep(2)

    await send_welcome(message=message, state=state)

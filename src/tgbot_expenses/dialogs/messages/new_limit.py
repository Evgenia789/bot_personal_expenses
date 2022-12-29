import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.callbacks.start_or_continue import (
    callbacks_continue, callbacks_start_over)
from src.tgbot_expenses.dialogs.messages.invalid_amount import message_invalid_amount
from src.tgbot_expenses.dialogs.commands.start import send_welcome
from src.tgbot_expenses.states.states_settings import StateSettings



@Bot.message_handler(state=StateSettings.NewLimit, content_types=types.ContentType.ANY)
async def message_limit(message: types.Message, state: FSMContext) -> None:
    """
    Process of setting new limit.
    """
    await Bot.delete_messages(message.chat.id, message.message_id, 2)

    if not message.text.isdigit():
        await StateSettings.InvalidAmount.set()
        await message_invalid_amount(message, state)
    else:
        async with state.proxy() as data:
            current_category = data["current_category"]

        database.update_limit(category_name=current_category, new_limit=message.text)

        last_message = await Bot.answer(
            message,
            f"Limit updated. Category: {current_category} \nNew limit: {message.text}"
        )

        await asyncio.sleep(2)

        await state.reset_data()

        await send_welcome(last_message, state)
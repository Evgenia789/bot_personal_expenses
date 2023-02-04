import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.dialogs.commands.start import send_welcome
from src.tgbot_expenses.dialogs.messages.invalid_amount import \
    message_invalid_amount
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.message_handler(state=StateSettings.CategoryLimit,
                     content_types=types.ContentType.ANY)
async def message_input_new_category(message: types.Message,
                                     state: FSMContext) -> None:
    """
    Process of input a category limit.
    """
    await Bot.delete_messages(chat_id=message.chat.id,
                              last_message_id=message.message_id, count=2)

    if not message.text.isdigit():
        await StateSettings.InvalidAmount.set()
        await message_invalid_amount(message, state)
    else:
        async with state.proxy() as data:
            name_new_category = data["category_name"]

        database.insert_category(category_name=name_new_category,
                                 limit_amount=message.text)

        message = await Bot.answer(
            message=message,
            text=f"Category {name_new_category} added"
        )

        await asyncio.sleep(2)

        await send_welcome(message=message, state=state)

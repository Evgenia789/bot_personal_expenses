import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.bot import Bot
from src.tgbot_expenses.constants import QuestionText
from src.tgbot_expenses.dialogs.callbacks.start_or_continue import (
    callbacks_continue, callbacks_start_over)
from src.tgbot_expenses.helpers.keyboards.back_or_main_menu import \
    get_keyboard_back_or_main_menu
from src.tgbot_expenses.database.db import database
from src.tgbot_expenses.states.states_chat import StateChat
from src.tgbot_expenses.states.states_settings import StateSettings


@Bot.message_handler(state=[StateChat.InvalidAmount, StateSettings.InvalidAmount], content_types=types.ContentType.ANY)
async def message_invalid_amount(message: types.Message, state: FSMContext) -> None:
    """
    Process a message about an invalid expense amount format.
    """
    msg = await message.answer(QuestionText.warning_number)
    current_state = await Bot.get_current_state()
    current_state_name = current_state.split(":")[0]

    await asyncio.sleep(2)

    await msg.delete()

    if current_state_name == "StateChat":
        await StateChat.Amount.set()
        await Bot.answer(message, QuestionText.amount)
    else:
        await StateSettings.NewLimit.set()
        async with state.proxy() as data:
            limit_category = data["limit_category"]
        await Bot.answer(
            message,
            f"Current limit: {limit_category}\nSend a new limit for category",
            reply_markup=str(get_keyboard_back_or_main_menu(main_menu_button=False))
        )
    

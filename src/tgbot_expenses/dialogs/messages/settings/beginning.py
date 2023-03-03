import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.tgbot_expenses.dialogs.commands.start import send_welcome


async def go_back_to_main_menu(message: types.Message,
                               state: FSMContext) -> None:
    """
    Reset the conversation state and send the user back to the main menu.

    :param message: The Message object containing the user's input message.
    :type message: types.Message
    :param state: The FSMContext object representing the current state
                  of the chat.
    :type state: FSMContext
    :return: None
    """
    await asyncio.sleep(2)

    await state.reset_data()

    await send_welcome(message=message, state=state)
